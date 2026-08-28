from rest_framework import serializers

from .config import is_secret_field
from .models import PlatformSetting

# Valeurs sentinelles pour les secrets non definis
MASKED = "••••••••"
EMPTY = ""


class PlatformSettingSerializer(serializers.ModelSerializer):
    """Serialiseur pour GET/PUT de la configuration.

    Les champs secrets (cle API, mots de passe) sont renvoyes masques.
    A l'ecriture, une valeur vide ou masquee conserve la valeur existante.
    """

    class Meta:
        model = PlatformSetting
        fields = [
            "llm_api_key",
            "llm_api_base_url",
            "llm_model",
            "email_host",
            "email_port",
            "email_host_user",
            "email_host_password",
            "email_use_tls",
            "email_from",
            "imap_host",
            "imap_port",
            "imap_user",
            "imap_password",
        ]

    def to_representation(self, obj):
        data = super().to_representation(obj)
        for field in self.Meta.fields:
            raw = getattr(obj, field, None)
            if is_secret_field(field):
                data[field] = MASKED if raw else EMPTY
                data[f"{field}_is_set"] = bool(raw)
        return data

    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            if field not in validated_data:
                continue
            value = validated_data[field]
            if is_secret_field(field) and (
                value == MASKED or not value or value == ""
            ):
                continue
            setattr(instance, field, value)
        instance.save()
        return instance
