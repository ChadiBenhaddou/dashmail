from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PlatformSetting
from .serializers import PlatformSettingSerializer


class IsAdminUser(permissions.BasePermission):
    """Autorise uniquement les staff/superuser."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )


class SettingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        obj = PlatformSetting.get_solo()
        return Response(PlatformSettingSerializer(obj).data)

    def put(self, request):
        obj = PlatformSetting.get_solo()
        serializer = PlatformSettingSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        from .config import apply_settings_to_django

        apply_settings_to_django()

        return Response(PlatformSettingSerializer(obj).data, status=status.HTTP_200_OK)
