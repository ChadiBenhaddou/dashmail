from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardView, ReportViewSet

router = DefaultRouter()
router.register(r"reports", ReportViewSet)

urlpatterns = [
    path("dashboard/<uuid:dashboard_uuid>/", DashboardView.as_view(), name="dashboard"),
    path("", include(router.urls)),
]
