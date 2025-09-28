import shortuuid
from typing import Any, cast, override
from django.db import models
from django.core.exceptions import ValidationError


class ShortUUIDField(models.CharField):
    """
    A Django CharField that stores a short UUID string generated using the
    shortuuid lib. The field auto-generates unique values on save with
    optional collision detection and retry logic.

    Attributes:
        auto (bool): If True, generates UUID automatically on model save.
        length (int): Length of the short UUID string (default 22).
        prefix (str): Optional string prefix prepended to the UUID.
        max_retries (int): Number of attempts to generate a unique UUID before raising.
        collision_check (bool): Whether to check for collisions in the DB.

    Raises:
        django.core.exceptions.ValidationError: Raised if unable to generate a unique
            short UUID after the configured number of retries.
    """

    def __init__(
        self,
        auto: bool = True,
        length: int = 22,
        prefix: str = "",
        max_retries: int = 10,
        collision_check: bool = True,
        *args: Any,
        **kwargs: Any,
    ):
        self.auto: bool = auto
        self.length: int = length
        self.prefix: str = prefix
        self.max_retries: int = max_retries
        self.collision_check: bool = collision_check

        max_length = len(prefix) + self.length
        kwargs.setdefault("max_length", max_length)
        if auto:
            kwargs.setdefault("editable", False)
            kwargs.setdefault("blank", True)
            kwargs.setdefault("unique", True)

        super().__init__(*args, **kwargs)

    def generate_uuid(self) -> str:
        """Generate a single short UUID string with prefix."""
        return self.prefix + shortuuid.ShortUUID().random(length=self.length)

    def generate_unique_uuid(self, model_instance: Any) -> str:
        """Try generating a unique UUID, checking DB collisions up to max_retries."""
        if not self.collision_check:
            return self.generate_uuid()

        for _ in range(self.max_retries):
            value = self.generate_uuid()
            if not model_instance.__class__.objects.filter(
                **{cast(str, self.attname): value}
            ).exists():
                return value
        raise ValidationError(
            f"Could not generate unique {self.attname} after {self.max_retries} attempts"
        )

    @override
    def pre_save(self, model_instance: Any, add: bool) -> Any:
        """On model save, generate and assign unique UUID if needed."""
        value = super().pre_save(model_instance, add)
        if self.auto and (value is None or value == ""):
            value = self.generate_unique_uuid(model_instance)
            setattr(model_instance, cast(str, self.attname), value)
        return value

    @override
    def formfield(self, **kwargs: Any) -> Any:
        """Return a disabled form field to show but prevent editing."""
        form_field = super().formfield(**kwargs)
        if form_field:
            form_field.disabled = True
        return form_field
