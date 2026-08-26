from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report
from .serializers import ReportSerializer
from .services.cache_service import get_cached_dashboard, set_cached_dashboard


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


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
