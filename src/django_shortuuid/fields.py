from typing import Any, cast, override
from django.db import models
from django.core.exceptions import ValidationError
import shortuuid


class ShortUUIDField(models.CharField):
    def __init__(
        self,
        auto: bool = True,
        length: int = 22,
        prefix: str = "",
        max_retries: int = 10,
        collision_check: bool = True,
        alphabet: str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.auto: bool = auto
        self.length: int = length
        self.prefix: str = prefix
        self.max_retries: int = max_retries
        self.collision_check: bool = collision_check
        self.alphabet: str | None = alphabet

        max_length = len(prefix) + length
        kwargs.setdefault("max_length", max_length)

        if auto:
            kwargs.setdefault("editable", False)
            kwargs.setdefault("blank", True)
            kwargs.setdefault("unique", True)

        super().__init__(*args, **kwargs)

    def _generate_shortuuid(self):
        """Generate a short UUID string using configured alphabet and prefix."""
        su = shortuuid.ShortUUID(alphabet=self.alphabet)
        return self.prefix + su.random(length=self.length)

    def generate_unique_shortuuid(self, model_instance: Any) -> str:
        """Generate unique UUID checking DB for collisions."""
        if not self.collision_check:
            return self._generate_shortuuid()

        for _ in range(self.max_retries):
            value = self._generate_shortuuid()
            if not model_instance.__class__.objects.filter(
                **{cast(str, self.attname): value}
            ).exists():
                return value
        raise ValidationError(
            f"Could not generate unique {self.attname} after {self.max_retries} attempts"
        )

    @override
    def pre_save(self, model_instance: Any, add: bool) -> Any:
        value = super().pre_save(model_instance, add)

        if self.auto and (value is None or value == ""):
            value = self.generate_unique_shortuuid(model_instance)
            setattr(model_instance, cast(str, self.attname), value)
        return value

    @override
    def deconstruct(
        self,
    ) -> tuple[Any | None, str, list[Any], dict[Any, Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs["length"] = self.length
        kwargs["prefix"] = self.prefix
        kwargs["max_retries"] = self.max_retries
        kwargs["collision_check"] = self.collision_check
        kwargs["alphabet"] = self.alphabet
        return name, path, args, kwargs
