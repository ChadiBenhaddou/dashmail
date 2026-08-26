from django.core.management.base import BaseCommand

from reports.services.email_ingestion import check_email_inbox


class Command(BaseCommand):
    help = "Manually check email inbox for report attachments"

    def handle(self, *args, **options):
        self.stdout.write("Checking email inbox...")
        result = check_email_inbox()
        self.stdout.write(
            self.style.SUCCESS(
                f"Email check complete: {result['processed']} report(s) created"
            )
        )
        if result["errors"]:
            self.stdout.write(self.style.WARNING(f"Errors: {result['errors']}"))
