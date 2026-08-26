"""
Centralized error handling for the report processing pipeline.
Maps exceptions to user-friendly French messages and Report status.
"""


class ReportError(Exception):
    """Base exception for report processing errors."""

    def __init__(self, message, user_message, status="failed"):
        self.message = message
        self.user_message = user_message
        self.status = status
        super().__init__(message)


class FileFormatError(ReportError):
    """Invalid or unsupported file format."""

    def __init__(self, detail=""):
        super().__init__(
            message=f"Format de fichier invalide: {detail}",
            user_message="Le fichier envoyé n'est pas au format CSV ou Excel accepté. Veuillez envoyer un fichier .csv, .xlsx ou .xls.",
            status="failed",
        )


class FileCorruptedError(ReportError):
    """File is corrupted or unreadable."""

    def __init__(self, detail=""):
        super().__init__(
            message=f"Fichier corrompu: {detail}",
            user_message="Le fichier semble corrompu ou illisible. Veuillez renvoyer le fichier.",
            status="failed",
        )


class LLMTimeoutError(ReportError):
    """LLM API call timed out."""

    def __init__(self):
        super().__init__(
            message="Timeout de l'appel LLM",
            user_message="L'analyse IA prend trop de temps. Veuillez réessayer ultérieurement.",
            status="failed",
        )


class LLMFormatError(ReportError):
    """LLM returned invalid JSON."""

    def __init__(self, detail=""):
        super().__init__(
            message=f"Réponse LLM mal formée: {detail}",
            user_message="L'analyse IA a retourné un résultat invalide. Veuillez réessayer.",
            status="failed",
        )


class NoColumnsError(ReportError):
    """No recognizable columns in the file."""

    def __init__(self):
        super().__init__(
            message="Aucune colonne reconnue",
            user_message="Le fichier ne contient pas de données tabulaires reconnues. Vérifiez le format.",
            status="failed",
        )


def handle_pipeline_error(exc, report):
    """Maps any exception to appropriate Report error state."""
    from django.utils import timezone

    if isinstance(exc, ReportError):
        report.status = "failed"
        report.error_message = exc.user_message
    else:
        report.status = "failed"
        report.error_message = (
            "Une erreur inattendue est survenue lors du traitement. Veuillez réessayer."
        )

    report.processed_at = timezone.now()
    report.save(update_fields=["status", "error_message", "processed_at"])
    return report
