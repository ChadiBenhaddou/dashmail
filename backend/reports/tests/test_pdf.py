from django.test import TestCase

from reports.models import Report
from reports.services.pdf_generator import generate_report_pdf


class PDFGeneratorTest(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            title="Test PDF Report",
            status="completed",
            row_count=100,
            column_count=5,
            data_quality_score=88.0,
            charts_config=[
                {"type": "bar", "title": "Ventes", "xAxisKey": "region", "yAxisKey": "sales", "data": [
                    {"region": "Nord", "sales": 100},
                    {"region": "Sud", "sales": 200},
                ]},
            ],
            llm_insights={
                "insights": [
                    {"title": "Test", "description": "Description test", "sentiment": "positive"},
                ],
                "summary": "Résumé test",
            },
        )

    def test_pdf_generation(self):
        response = generate_report_pdf(self.report)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_pdf_content_disposition(self):
        response = generate_report_pdf(self.report)
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("rapport-", response["Content-Disposition"])

    def test_pdf_with_no_charts(self):
        self.report.charts_config = []
        response = generate_report_pdf(self.report)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_pdf_with_string_insights(self):
        self.report.llm_insights = "Simple text insight"
        response = generate_report_pdf(self.report)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
