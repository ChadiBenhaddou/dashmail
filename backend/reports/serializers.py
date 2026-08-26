from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "source_file",
            "status",
            "dashboard_link",
            "row_count",
            "column_count",
            "file_size",
            "llm_insights",
            "charts_config",
            "data_quality_score",
            "cleaning_log",
            "error_message",
            "sender_email",
            "created_at",
            "updated_at",
            "processed_at",
        ]
        read_only_fields = [
            "id",
            "dashboard_link",
            "status",
            "created_at",
            "updated_at",
        ]
