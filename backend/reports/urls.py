from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardView, ReportViewSet, StatsView, UploadView

router = DefaultRouter()
router.register(r"reports", ReportViewSet)

urlpatterns = [
    path("dashboard/<uuid:dashboard_uuid>/", DashboardView.as_view(), name="dashboard"),
    path("reports/upload/", UploadView.as_view(), name="upload"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("", include(router.urls)),
]
