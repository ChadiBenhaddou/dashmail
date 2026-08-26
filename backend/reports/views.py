from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report
from .serializers import ReportSerializer
from .services.cache_service import get_cached_dashboard, set_cached_dashboard
from .services.pdf_generator import generate_report_pdf


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(sender_email=self.request.user.email).order_by("-created_at")


class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    MAX_FILE_SIZE = 20 * 1024 * 1024
    ALLOWED_TYPES = [".csv", ".xlsx", ".xls"]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "Aucun fichier fourni."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ext = "." + file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
        if ext not in self.ALLOWED_TYPES:
            return Response(
                {"error": f"Format non supporté. Formats acceptés : {', '.join(self.ALLOWED_TYPES)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if file.size > self.MAX_FILE_SIZE:
            return Response(
                {"error": f"Fichier trop volumineux. Taille maximale : {self.MAX_FILE_SIZE // (1024*1024)} Mo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = request.data.get("title", "").strip() or file.name.rsplit(".", 1)[0]

        report = Report.objects.create(
            title=title,
            sender_email=request.user.email,
            file_size=file.size,
            status=Report.Status.PENDING,
        )

        from reports.models import DataFile
        DataFile.objects.create(
            report=report,
            file=file,
            original_filename=file.name,
            file_type=ext.lstrip("."),
        )

        from .tasks import process_report
        process_report.delay(str(report.id))

        return Response(
            {
                "id": str(report.id),
                "dashboard_link": str(report.dashboard_link),
                "status": report.status,
                "message": "Fichier uploadé. Traitement en cours...",
            },
            status=status.HTTP_201_CREATED,
        )


class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, dashboard_uuid):
        cached = get_cached_dashboard(dashboard_uuid)
        if cached is not None:
            return Response(cached)

        try:
            report = Report.objects.get(dashboard_link=dashboard_uuid)
        except Report.DoesNotExist:
            return Response(
                {"error": "Rapport non trouvé", "code": "not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if report.status == "failed":
            return Response(
                {"error": report.error_message or "Traitement échoué", "code": "processing_failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if report.status != "completed":
            return Response(
                {"status": report.status, "message": "Rapport en cours de traitement"},
                status=status.HTTP_202_ACCEPTED,
            )

        kpis = _generate_kpis(report)

        payload = {
            "report": {
                "id": str(report.id),
                "title": report.title,
                "status": report.status,
                "source_filename": (
                    report.source_file.name.split("/")[-1]
                    if report.source_file
                    else ""
                ),
                "row_count": report.row_count,
                "column_count": report.column_count,
                "file_size": report.file_size,
                "download_url": (
                    request.build_absolute_uri(report.source_file.url)
                    if report.source_file
                    else None
                ),
                "created_at": report.created_at.isoformat(),
                "processed_at": (
                    report.processed_at.isoformat()
                    if report.processed_at
                    else None
                ),
            },
            "charts": report.charts_config or [],
            "insights": report.llm_insights or {},
            "data_quality": {
                "score": report.data_quality_score,
                "cleaning_log": report.cleaning_log or {},
            },
            "kpis": kpis,
        }

        set_cached_dashboard(dashboard_uuid, payload)

        return Response(payload)


def _generate_kpis(report):
    kpis = []
    if report.charts_config:
        for chart in report.charts_config[:4]:
            data = chart.get("data", [])
            y_key = chart.get("yAxisKey", "value")
            if data:
                total = sum(d.get(y_key, 0) for d in data)
                prev_total = total * 0.85
                variation = round(((total - prev_total) / prev_total * 100), 1) if prev_total else 0
                kpis.append({
                    "label": chart.get("title", "Indicateur"),
                    "value": round(total, 2),
                    "variation": variation,
                })
    return kpis


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_reports = Report.objects.filter(sender_email=request.user.email)
        total = user_reports.count()
        completed = user_reports.filter(status=Report.Status.COMPLETED).count()
        failed = user_reports.filter(status=Report.Status.FAILED).count()
        processing = total - completed - failed
        total_size = sum(r.file_size or 0 for r in user_reports)
        recent = user_reports.order_by("-created_at")[:5]

        return Response({
            "total": total,
            "completed": completed,
            "failed": failed,
            "processing": processing,
            "total_size_bytes": total_size,
            "recent_reports": [
                {
                    "id": str(r.id),
                    "title": r.title,
                    "status": r.status,
                    "created_at": r.created_at.isoformat(),
                    "row_count": r.row_count,
                    "dashboard_link": str(r.dashboard_link),
                }
                for r in recent
            ],
        })


class ReportPDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, dashboard_uuid):
        report = get_object_or_404(Report, dashboard_link=dashboard_uuid)
        if report.status != Report.Status.COMPLETED:
            return Response(
                {"error": "Le rapport n'est pas encore terminé."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pdf_response = generate_report_pdf(report)
        if pdf_response is None:
            return Response(
                {"error": "Erreur lors de la génération du PDF."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return pdf_response
