import uuid

from django.db import models


class Report(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PARSING = "parsing", "Parsing"
        ANALYZING = "analyzing", "Analyzing"
        GENERATING = "generating", "Generating"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    source_file = models.FileField(upload_to="reports/")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    dashboard_link = models.UUIDField(unique=True, default=uuid.uuid4)
    row_count = models.PositiveIntegerField(null=True, blank=True)
    column_count = models.PositiveIntegerField(null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    llm_insights = models.JSONField(null=True, blank=True)
    charts_config = models.JSONField(null=True, blank=True)
    data_quality_score = models.FloatField(null=True, blank=True)
    cleaning_log = models.JSONField(null=True, blank=True)
    kpi_config = models.JSONField(null=True, blank=True)
    computed_kpis = models.JSONField(null=True, blank=True)
    dashboard_profile = models.JSONField(null=True, blank=True)
    custom_prompt = models.TextField(blank=True, default="")
    error_message = models.TextField(blank=True, default="")
    sender_email = models.EmailField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return self.title


class DataFile(models.Model):
    class ParsingStatus(models.TextChoices):
        RECEIVED = "received", "Received"
        PARSING = "parsing", "Parsing"
        PARSED = "parsed", "Parsed"
        ERROR = "error", "Error"

    id = models.BigAutoField(primary_key=True)
    report = models.OneToOneField(
        Report, on_delete=models.CASCADE, related_name="data_file"
    )
    file = models.FileField(upload_to="data_files/")
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    parsing_status = models.CharField(
        max_length=20, choices=ParsingStatus.choices, default=ParsingStatus.RECEIVED
    )
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Data File"
        verbose_name_plural = "Data Files"

    def __str__(self):
        return self.original_filename
