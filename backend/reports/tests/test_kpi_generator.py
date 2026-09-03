import pandas as pd

from django.test import TestCase

from reports.services.kpi_generator import compute_kpis


class KpiGeneratorTest(TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "m": ["a", "a", "b", "b"],
            "v": [10, 20, 30, 40],
        })

    def test_sum_kpi(self):
        config = [{"label": "Total", "x_axis": "m", "y_axis": "v", "calculation": "sum"}]
        kpis = compute_kpis(self.df, config)
        self.assertEqual(len(kpis), 1)
        self.assertEqual(kpis[0]["value"], 100)

    def test_mean_kpi(self):
        config = [{"label": "Moyenne", "x_axis": "m", "y_axis": "v", "calculation": "mean"}]
        kpis = compute_kpis(self.df, config)
        self.assertEqual(kpis[0]["value"], 25)

    def test_count_kpi(self):
        config = [{"label": "Comptage", "x_axis": "m", "y_axis": "v", "calculation": "count"}]
        kpis = compute_kpis(self.df, config)
        self.assertEqual(kpis[0]["value"], 4)

    def test_empty_config_falls_back(self):
        kpis = compute_kpis(self.df, [])
        self.assertTrue(len(kpis) >= 1)
        self.assertEqual(kpis[-1]["label"], "Lignes")
        self.assertEqual(kpis[-1]["value"], 4)

    def test_date_variation_computed(self):
        df = pd.DataFrame({
            "date": ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01", "2024-05-01", "2024-06-01"],
            "v": [10, 10, 10, 20, 20, 20],
        })
        config = [{"label": "Total", "x_axis": "date", "y_axis": "v", "calculation": "sum"}]
        kpis = compute_kpis(df, config)
        self.assertIn("variation", kpis[0])
        self.assertAlmostEqual(kpis[0]["variation"], 100.0, places=5)

    def test_capped_at_four(self):
        df = pd.DataFrame({"m": ["a", "b"], "v": [1, 2]})
        config = [
            {"label": f"K{i}", "x_axis": "m", "y_axis": "v", "calculation": "sum"}
            for i in range(10)
        ]
        kpis = compute_kpis(df, config)
        self.assertLessEqual(len(kpis), 4)
