import csv
import os
import tempfile

from django.test import TestCase

from reports.services.data_parser import parse_file


class DataParserTest(TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        writer = csv.writer(self.tmp)
        writer.writerow(["Date", "Region", "Ventes", "Produit"])
        writer.writerow(["2024-01-01", "Nord", "1500", "A"])
        writer.writerow(["2024-01-02", "Sud", "2000", "B"])
        writer.writerow(["2024-01-03", "Nord", "1800", "A"])
        writer.writerow(["2024-01-04", "", "2200", "C"])  # missing region
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_parse_csv(self):
        result = parse_file(self.tmp.name)
        self.assertEqual(result["row_count"], 4)
        self.assertEqual(result["column_count"], 4)
        self.assertEqual(result["file_type"], "csv")

    def test_detect_numeric(self):
        result = parse_file(self.tmp.name)
        self.assertIn("Ventes", result["numeric_columns"])

    def test_detect_missing(self):
        result = parse_file(self.tmp.name)
        self.assertGreater(result["missing_total"], 0)
