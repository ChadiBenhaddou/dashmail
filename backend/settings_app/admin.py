from django.contrib import admin

from .models import PlatformSetting


@admin.register(PlatformSetting)
class PlatformSettingAdmin(admin.ModelAdmin):
    verbose_name = "Configuration plateforme"
    verbose_name_plural = "Configuration plateforme"
