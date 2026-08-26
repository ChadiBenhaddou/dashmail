"""
End-to-end test script for Dashbail.
Tests the full flow: file upload → processing → dashboard display.

Usage: Run with Django test runner or standalone.
"""
import os
import sys
import csv
import tempfile
import uuid

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

import django
django.setup()

from django.test import TestCase, Client
from reports.models import Report, DataFile
from reports.services.data_parser import parse_file
from reports.services.data_cleaner import clean_data
from reports.services.llm_prompt import build_analysis_prompt
import pandas as pd


class TestFullFlow(TestCase):
    """Test the complete report generation flow."""
    
    def setUp(self):
        self.client = Client()
        # Create test CSV data
        self.test_data = [
            ['Date', 'Region', 'Produit', 'Ventes', 'Montant'],
            ['2024-01-01', 'Île-de-France', 'Produit A', '150', '15000'],
            ['2024-01-02', 'Occitanie', 'Produit B', '200', '25000'],
            ['2024-01-03', 'Île-de-France', 'Produit A', '180', '18000'],
            ['2024-01-04', 'Auvergne-Rhône-Alpes', 'Produit C', '120', '9600'],
            ['2024-01-05', 'Occitanie', 'Produit A', '220', '22000'],
            ['2024-01-06', 'Île-de-France', 'Produit B', '190', '23750'],
            ['2024-01-07', 'Auvergne-Rhône-Alpes', 'Produit A', '160', '16000'],
            ['2024-01-08', 'Occitanie', 'Produit C', '140', '11200'],
            ['2024-01-09', 'Île-de-France', 'Produit A', '210', '21000'],
            ['2024-01-10', 'Auvergne-Rhône-Alpes', 'Produit B', '175', '21875'],
        ]
    
    def create_test_csv(self):
        """Create a temporary CSV file with test data."""
        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        )
        writer = csv.writer(tmp)
        writer.writerows(self.test_data)
        tmp.close()
        return tmp.name
    
    def test_01_parse_csv(self):
        """Test CSV parsing."""
        csv_path = self.create_test_csv()
        try:
            result = parse_file(csv_path)
            self.assertEqual(result['row_count'], 10)
            self.assertEqual(result['column_count'], 5)
            self.assertEqual(result['file_type'], 'csv')
            self.assertIn('Ventes', result['numeric_columns'])
            self.assertIn('Region', result['categorical_columns'])
            print(f"✓ Parse: {result['row_count']} rows, {result['column_count']} columns")
        finally:
            os.unlink(csv_path)
    
    def test_02_clean_data(self):
        """Test data cleaning."""
        csv_path = self.create_test_csv()
        try:
            result = parse_file(csv_path)
            # Read with pandas to get a DataFrame
            df = pd.read_csv(csv_path)
            cleaned, log = clean_data(df)
            self.assertIsInstance(cleaned, pd.DataFrame)
            self.assertIn('duplicates_removed', log)
            print(f"✓ Clean: {len(cleaned)} rows after cleaning, log: {log}")
        finally:
            os.unlink(csv_path)
    
    def test_03_build_prompt(self):
        """Test LLM prompt generation."""
        csv_path = self.create_test_csv()
        try:
            result = parse_file(csv_path)
            system_prompt, user_prompt = build_analysis_prompt(result)
            self.assertIn('JSON', system_prompt)
            self.assertIn('Ventes', user_prompt)
            self.assertIn('Region', user_prompt)
            print(f"✓ Prompt: system={len(system_prompt)} chars, user={len(user_prompt)} chars")
        finally:
            os.unlink(csv_path)
    
    def test_04_create_report(self):
        """Test Report model creation."""
        report = Report.objects.create(
            title="Test E2E Report",
            status="completed",
            row_count=10,
            column_count=5,
            charts_config=[
                {
                    "type": "bar",
                    "title": "Ventes par région",
                    "data": [
                        {"Region": "Île-de-France", "Ventes": 540},
                        {"Region": "Occitanie", "Ventes": 560},
                        {"Region": "Auvergne-Rhône-Alpes", "Ventes": 295}
                    ],
                    "xAxisKey": "Region",
                    "yAxisKey": "Ventes"
                }
            ],
            llm_insights={
                "insights": [
                    {"title": "Leader régional", "description": "L'Occitanie domine les ventes.", "sentiment": "positive"},
                    {"title": "Croissance", "description": "Tendance à la hausse sur la période.", "sentiment": "positive"}
                ],
                "summary": "Les ventes sont en hausse de 15% sur la période analysée."
            },
            data_quality_score=92.0,
        )
        self.assertIsNotNone(report.dashboard_link)
        print(f"✓ Report created: {report.id}, dashboard: {report.dashboard_link}")
    
    def test_05_dashboard_endpoint(self):
        """Test the public dashboard API endpoint."""
        report = Report.objects.create(
            title="Test Dashboard",
            status="completed",
            charts_config=[],
            llm_insights={"summary": "Test"},
            data_quality_score=85.0,
        )
        response = self.client.get(f'/api/dashboard/{report.dashboard_link}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('report', data)
        self.assertIn('charts', data)
        self.assertIn('insights', data)
        self.assertIn('data_quality', data)
        print(f"✓ Dashboard endpoint: status={response.status_code}, keys={list(data.keys())}")
    
    def test_06_dashboard_not_found(self):
        """Test 404 for invalid dashboard UUID."""
        fake_uuid = uuid.uuid4()
        response = self.client.get(f'/api/dashboard/{fake_uuid}/')
        self.assertEqual(response.status_code, 404)
        print(f"✓ Not found: status={response.status_code}")
    
    def test_07_full_pipeline_simulation(self):
        """Simulate the full pipeline without LLM."""
        csv_path = self.create_test_csv()
        try:
            # Step 1: Parse
            parse_result = parse_file(csv_path)
            print(f"  1. Parsed: {parse_result['row_count']} rows")
            
            # Step 2: Clean
            df = pd.read_csv(csv_path)
            cleaned_df, clean_log = clean_data(df)
            print(f"  2. Cleaned: {len(cleaned_df)} rows, log={clean_log}")
            
            # Step 3: Build prompt
            system_prompt, user_prompt = build_analysis_prompt(parse_result)
            print(f"  3. Prompt built: {len(user_prompt)} chars")
            
            # Step 4: Create report (simulate LLM response)
            report = Report.objects.create(
                title="E2E Pipeline Test",
                status="completed",
                row_count=parse_result['row_count'],
                column_count=parse_result['column_count'],
                charts_config=[
                    {"type": "bar", "title": "Ventes", "data": [], "xAxisKey": "Region", "yAxisKey": "Ventes"}
                ],
                llm_insights={"summary": "Pipeline E2E réussi."},
                data_quality_score=parse_result.get('missing_pct', 0),
                cleaning_log=clean_log,
            )
            print(f"  4. Report: {report.id}")
            
            # Step 5: Verify dashboard endpoint
            response = self.client.get(f'/api/dashboard/{report.dashboard_link}/')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['report']['title'], 'E2E Pipeline Test')
            print(f"  5. Dashboard verified: {response.status_code}")
            print("✓ Full pipeline E2E test PASSED")
        finally:
            os.unlink(csv_path)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
