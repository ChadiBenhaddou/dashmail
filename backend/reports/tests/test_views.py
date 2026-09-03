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

    def test_dashboard_exposes_custom_prompt_and_pdf_url(self):
        self.report.custom_prompt = "Fais un camembert par region"
        self.report.save()
        response = self.client.get(f"/api/dashboard/{self.report.dashboard_link}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["report"]["custom_prompt"], "Fais un camembert par region")
        self.assertIn("/pdf/", data["report"]["pdf_url"])
        self.assertIn("data_quality", data)

    def test_dashboard_exposes_dashboard_fields(self):
        self.report.llm_insights = {
            "executive_summary": "Les ventes progressent.",
            "overall_sentiment": "positive",
            "insights": [],
        }
        self.report.computed_kpis = [
            {"label": "Total", "value": 300, "variation": 12.0},
        ]
        self.report.dashboard_profile = {
            "row_count": 2,
            "numeric_columns": [{"name": "sales", "min": 100, "max": 200, "mean": 150, "sum": 300}],
        }
        self.report.save()
        response = self.client.get(f"/api/dashboard/{self.report.dashboard_link}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["executive_summary"], "Les ventes progressent.")
        self.assertEqual(data["overall_sentiment"], "positive")
        self.assertEqual(data["kpis"][0]["label"], "Total")
        self.assertEqual(data["dashboard_profile"]["row_count"], 2)

    def test_dashboard_kpis_fallback_to_heuristic(self):
        self.report.computed_kpis = None
        self.report.charts_config = [
            {"title": "Ventes", "data": [{"region": "Nord", "sales": 100}], "yAxisKey": "sales"}
        ]
        self.report.save()
        response = self.client.get(f"/api/dashboard/{self.report.dashboard_link}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("kpis", data)


class UploadViewTest(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user(
            username="uploader", email="uploader@example.com", password="pass123"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def _make_csv(self, name="data.csv"):
        import io

        return io.BytesIO(
            b"region,sales\nnord,100\nsud,200\n"
        ), name

    def test_upload_stores_custom_prompt(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        csv_file, _ = self._make_csv()
        uploaded = SimpleUploadedFile(
            "data.csv",
            csv_file.getvalue(),
            content_type="text/csv",
        )
        response = self.client.post(
            "/api/reports/upload/",
            {
                "file": uploaded,
                "title": "Ventes",
                "custom_prompt": "Montre les ventes par region",
            },
        )
        self.assertEqual(response.status_code, 201)
        report = Report.objects.get(pk=response.json()["id"])
        self.assertEqual(report.custom_prompt, "Montre les ventes par region")
