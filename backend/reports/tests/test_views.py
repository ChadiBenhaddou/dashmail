import uuid

from django.test import Client, TestCase

from reports.models import Report


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.report = Report.objects.create(
            title="Test Report",
            status="completed",
            charts_config=[],
            llm_insights={"summary": "Test insight"},
            data_quality_score=85.0,
        )

    def test_dashboard_success(self):
        response = self.client.get(f"/api/dashboard/{self.report.dashboard_link}/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_not_found(self):
        fake_uuid = uuid.uuid4()
        response = self.client.get(f"/api/dashboard/{fake_uuid}/")
        self.assertEqual(response.status_code, 404)

    def test_dashboard_in_progress(self):
        self.report.status = "parsing"
        self.report.save()
        response = self.client.get(f"/api/dashboard/{self.report.dashboard_link}/")
        self.assertEqual(response.status_code, 202)
