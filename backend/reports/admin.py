from django.contrib import admin

from .models import DataFile, Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "sender_email",
        "row_count",
        "column_count",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("title", "sender_email")
    readonly_fields = (
        "id",
        "dashboard_link",
        "created_at",
        "updated_at",
        "processed_at",
    )


@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "report",
        "file_type",
        "parsing_status",
        "created_at",
    )
    list_filter = ("file_type", "parsing_status")
    search_fields = ("original_filename",)
    readonly_fields = ("created_at",)
