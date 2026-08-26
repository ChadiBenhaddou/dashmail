from django.test import TestCase
from reports.models import Report, DataFile


class ReportModelTest(TestCase):
    def test_create_report(self):
        report = Report.objects.create(title="Test Report")
        self.assertEqual(report.status, "pending")
        self.assertIsNotNone(report.dashboard_link)
        self.assertIsNotNone(report.id)

    def test_report_str(self):
        report = Report.objects.create(title="Ventes Q1")
        self.assertEqual(str(report), "Ventes Q1")

    def test_data_file_str(self):
        report = Report.objects.create(title="Test")
        data_file = DataFile.objects.create(
            report=report,
            original_filename="data.csv",
            file_type="csv",
        )
        self.assertEqual(str(data_file), "data.csv")
