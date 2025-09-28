from django.contrib import admin
from .models import DemoModel


@admin.register(DemoModel)
class DemoModelAdmin(admin.ModelAdmin):
    readonly_fields: tuple[str] = ("id",)
