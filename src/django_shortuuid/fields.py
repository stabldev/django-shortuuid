import shortuuid
from typing import Any, override
from django.db import models


class ShortUUIDField(models.CharField):
    def __init__(
        self,
        auto: bool = True,
        length: int = 22,
        prefix: str = "",
        *args: Any,
        **kwargs: Any,
    ):
        self.auto: bool = auto
        self.length: int = length
        self.prefix: str = prefix
        max_length = len(prefix) + self.length
        kwargs.setdefault("max_length", max_length)
        if auto:
            kwargs.setdefault("editable", False)
            kwargs.setdefault("blank", True)
            kwargs.setdefault("unique", True)
        super().__init__(*args, **kwargs)

    @override
    def pre_save(self, model_instance: Any, add: bool):
        value = super().pre_save(model_instance, add)
        if self.auto and not value:
            value = self.prefix + shortuuid.ShortUUID().random(length=self.length)
            setattr(model_instance, self.attname, value)  # pyright: ignore [reportArgumentType]
        return value

    @override
    def formfield(self, **kwargs: Any):
        form_field = super().formfield(**kwargs)
        if form_field:
            form_field.disabled = True
        return form_field
