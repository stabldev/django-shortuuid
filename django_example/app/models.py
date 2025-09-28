from django.db import models
from django_shortuuid.fields import ShortUUIDField


class DemoModel(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    id: ShortUUIDField = ShortUUIDField(
        prefix="id_",
        primary_key=True,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
        length=7,
    )
