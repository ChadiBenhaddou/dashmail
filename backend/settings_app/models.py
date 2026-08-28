from django.db import models


class PlatformSetting(models.Model):
    """Configuration unique (singleton) pour la plateforme.

    Ces valeurs, editees depuis l'interface admin, ont priorite sur les
    variables d'environnement. Si une valeur est laissee vide, le service
    retombe sur la variable d'environnement correspondante.
    """

    # LLM
    llm_api_key = models.TextField(blank=True, default="")
    llm_api_base_url = models.TextField(blank=True, default="")
    llm_model = models.CharField(max_length=120, blank=True, default="")

    # SMTP - envoi des rapports
    email_host = models.CharField(max_length=255, blank=True, default="")
    email_port = models.PositiveIntegerField(default=587)
    email_host_user = models.CharField(max_length=255, blank=True, default="")
    email_host_password = models.TextField(blank=True, default="")
    email_use_tls = models.BooleanField(default=True)
    email_from = models.EmailField(blank=True, default="")

    # IMAP - ingestion des fichiers par email
    imap_host = models.CharField(max_length=255, blank=True, default="")
    imap_port = models.PositiveIntegerField(default=993)
    imap_user = models.CharField(max_length=255, blank=True, default="")
    imap_password = models.TextField(blank=True, default="")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration plateforme"
        verbose_name_plural = "Configuration plateforme"

    def __str__(self):
        return "Configuration plateforme"

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
