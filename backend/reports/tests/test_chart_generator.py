import pandas as pd

from django.test import TestCase

from reports.services.chart_generator import generate_charts_config


class ChartGeneratorTest(TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "region": ["Nord", "Sud", "Est", "Ouest"],
            "sales": [100, 200, 150, 300],
            "revenue": [1000, 2000, 1500, 3000],
        })

    def test_bar_chart_generation(self):
        llm = {"visualizations": [{"type": "bar", "x_axis": "region", "y_axis": "sales", "title": "Ventes"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "bar")
        self.assertEqual(len(charts[0]["data"]), 4)

    def test_line_chart_generation(self):
        llm = {"visualizations": [{"type": "line", "x_axis": "region", "y_axis": "revenue", "title": "Revenu"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "line")

    def test_pie_chart_generation(self):
        llm = {"visualizations": [{"type": "pie", "x_axis": "region", "y_axis": "sales", "title": "Parts"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "pie")

    def test_invalid_axis_skipped(self):
        llm = {"visualizations": [{"type": "bar", "x_axis": "nonexistent", "y_axis": "sales", "title": "Test"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 0)

    def test_empty_visualizations(self):
        charts = generate_charts_config(self.df, {"visualizations": []})
        self.assertEqual(len(charts), 0)

    def test_multiple_charts(self):
        llm = {"visualizations": [
            {"type": "bar", "x_axis": "region", "y_axis": "sales", "title": "Ventes"},
            {"type": "line", "x_axis": "region", "y_axis": "revenue", "title": "Revenu"},
        ]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 2)
