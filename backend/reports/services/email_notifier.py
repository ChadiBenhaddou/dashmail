from django.core.mail import send_mail
from django.conf import settings


def send_success_email(report):
    """Send dashboard link email after successful report generation."""
    subject = f"Votre rapport '{report.title}' est prêt"
    dashboard_url = f"{settings.FRONTEND_URL}/dashboard/{report.dashboard_link}"
    message = f"""
Bonjour,

Votre rapport "{report.title}" a été généré avec succès.

Vous pouvez le consulter en cliquant sur le lien ci-dessous :
{dashboard_url}

Ce lien est accessible sans compte. Il est valide pendant 7 jours.

Lignes analysées : {report.row_count or 'N/A'}
Qualité des données : {report.data_quality_score or 'N/A'}/100

Cordialement,
Dashboard X
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[report.sender_email],
            fail_silently=True,
        )
    except Exception:
        pass  # Don't fail the pipeline if email fails


def send_failure_email(report):
    """Send error notification email."""
    subject = f"Erreur lors du traitement de '{report.title}'"
    message = f"""
Bonjour,

Une erreur est survenue lors du traitement de votre fichier "{report.title}".

Raison : {report.error_message or "Erreur inconnue"}

Vous pouvez réessayer en envoyant à nouveau votre fichier par email.

Cordialement,
Dashboard X
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[report.sender_email],
            fail_silently=True,
        )
    except Exception:
        pass
