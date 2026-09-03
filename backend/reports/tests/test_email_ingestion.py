import email

from django.test import TestCase

from reports.services.email_ingestion import _extract_body


class EmailBodyExtractionTest(TestCase):
    def _make_message(self, text):
        msg = email.message.EmailMessage()
        msg["Subject"] = "Test"
        msg.set_content(text)
        return msg

    def test_extracts_plain_text(self):
        body = _extract_body(self._make_message("Fais un camembert par region."))
        self.assertIn("camembert", body)

    def test_strips_quoted_reply(self):
        msg = self._make_message(
            "Montre les ventes par mois.\n> Le fichier precedent ne convenait pas."
        )
        body = _extract_body(msg)
        self.assertIn("par mois", body)
        self.assertNotIn("precedent", body)

    def test_strips_signature(self):
        msg = self._make_message("Compare les revenus.\n-- \nBien a vous, Jean")
        body = _extract_body(msg)
        self.assertIn("Compare", body)
        self.assertNotIn("Jean", body)

    def test_empty_when_no_body(self):
        msg = email.message.EmailMessage()
        self.assertEqual(_extract_body(msg), "")
