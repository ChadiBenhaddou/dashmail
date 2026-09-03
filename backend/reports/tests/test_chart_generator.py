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

    def test_custom_chart_sum(self):
        llm = {
            "visualizations": [],
            "custom_visualizations": [
                {"type": "bar", "x_axis": "region", "y_axis": "sales", "title": "Total", "calculation": "sum"}
            ],
        }
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertTrue(charts[0]["custom"])
        total = sum(d["sales"] for d in charts[0]["data"])
        self.assertEqual(total, 750)

    def test_custom_chart_count(self):
        llm = {
            "visualizations": [],
            "custom_visualizations": [
                {"type": "pie", "x_axis": "region", "y_axis": "count", "title": "Compte", "calculation": "count"}
            ],
        }
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        counts = {d["region"]: d["count"] for d in charts[0]["data"]}
        self.assertEqual(counts["Nord"], 1)

    def test_custom_chart_mean(self):
        self.df = pd.DataFrame({
            "m": ["a", "a", "b"],
            "v": [10, 30, 90],
        })
        llm = {
            "visualizations": [],
            "custom_visualizations": [
                {"type": "bar", "x_axis": "m", "y_axis": "v", "title": "Moyenne", "calculation": "mean"}
            ],
        }
        charts = generate_charts_config(self.df, llm)
        data = {d["m"]: d["v"] for d in charts[0]["data"]}
        self.assertEqual(data["a"], 20)

    def test_custom_chart_appended_after_auto(self):
        llm = {
            "visualizations": [
                {"type": "bar", "x_axis": "region", "y_axis": "sales", "title": "Auto"}
            ],
            "custom_visualizations": [
                {"type": "bar", "x_axis": "region", "y_axis": "revenue", "title": "Custom", "calculation": "sum"}
            ],
        }
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 2)
        self.assertEqual(charts[0]["title"], "Auto")
        self.assertEqual(charts[1]["title"], "Custom")
        self.assertTrue(charts[1]["custom"])

    def test_custom_chart_invalid_axis_skipped(self):
        llm = {
            "visualizations": [],
            "custom_visualizations": [
                {"type": "bar", "x_axis": "nope", "y_axis": "sales", "title": "Bad", "calculation": "sum"}
            ],
        }
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 0)

    def test_area_chart_generation(self):
        llm = {"visualizations": [{"type": "area", "x_axis": "region", "y_axis": "sales", "title": "Aire"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "area")
        self.assertEqual(len(charts[0]["data"]), 4)

    def test_scatter_chart_generation(self):
        llm = {"visualizations": [{"type": "scatter", "x_axis": "sales", "y_axis": "revenue", "title": "Corrélation"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "scatter")
        self.assertEqual(len(charts[0]["data"]), 4)

    def test_radar_chart_generation(self):
        llm = {"visualizations": [{"type": "radar", "x_axis": "region", "y_axis": "sales", "title": "Radar"}]}
        charts = generate_charts_config(self.df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "radar")
        self.assertEqual(len(charts[0]["data"]), 4)

    def test_grouped_multi_series_bar(self):
        df = pd.DataFrame({
            "month": ["Jan", "Jan", "Feb", "Feb", "Mar"],
            "product": ["A", "B", "A", "B", "A"],
            "sales": [10, 20, 30, 40, 50],
        })
        llm = {"visualizations": [
            {"type": "bar", "x_axis": "month", "y_axis": "sales",
             "group": "product", "title": "Ventes par produit", "calculation": "sum"}
        ]}
        charts = generate_charts_config(df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0]["type"], "bar")
        self.assertIn("seriesKeys", charts[0])
        self.assertEqual(set(charts[0]["seriesKeys"]), {"A", "B"})
        self.assertEqual(len(charts[0]["data"]), 3)

    def test_grouped_multi_series_line(self):
        df = pd.DataFrame({
            "month": ["Jan", "Jan", "Feb", "Feb"],
            "product": ["A", "B", "A", "B"],
            "sales": [10, 20, 30, 40],
        })
        llm = {"visualizations": [
            {"type": "line", "x_axis": "month", "y_axis": "sales",
             "group": "product", "title": "Évolutions", "calculation": "sum"}
        ]}
        charts = generate_charts_config(df, llm)
        self.assertEqual(len(charts), 1)
        self.assertEqual(set(charts[0]["seriesKeys"]), {"A", "B"})

    def test_only_one_pie_allowed(self):
        llm = {"visualizations": [
            {"type": "pie", "x_axis": "region", "y_axis": "sales", "title": "Pie1"},
            {"type": "pie", "x_axis": "region", "y_axis": "revenue", "title": "Pie2"},
        ]}
        charts = generate_charts_config(self.df, llm)
        pies = [c for c in charts if c.get("type") == "pie"]
        self.assertLessEqual(len(pies), 1)

    def test_max_chart_cap(self):
        viz = [
            {"type": "bar", "x_axis": "region", "y_axis": col, "title": f"Chart {i}"}
            for i, col in enumerate(["sales", "revenue", "sales", "revenue", "sales", "revenue", "sales", "revenue", "sales"])
        ]
        llm = {"visualizations": viz[:9]}
        charts = generate_charts_config(self.df, llm)
        self.assertLessEqual(len(charts), 7)
        self.assertEqual(len(charts), 7)
