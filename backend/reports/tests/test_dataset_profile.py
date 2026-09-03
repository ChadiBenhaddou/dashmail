import pandas as pd

from django.test import TestCase

from reports.services.dataset_profile import build_dashboard_profile


class DatasetProfileTest(TestCase):
    def test_builds_numeric_and_categorical(self):
        df = pd.DataFrame({
            "sales": [100, 200, 300],
            "region": ["Nord", "Sud", "Nord"],
        })
        profile = build_dashboard_profile(df)
        self.assertEqual(profile["row_count"], 3)
        self.assertEqual(profile["column_count"], 2)
        self.assertEqual(len(profile["numeric_columns"]), 1)
        self.assertEqual(profile["numeric_columns"][0]["name"], "sales")
        self.assertEqual(profile["numeric_columns"][0]["sum"], 600)
        self.assertEqual(len(profile["categorical_columns"]), 1)
        top = profile["categorical_columns"][0]["top_values"]
        self.assertEqual(top[0]["value"], "Nord")
        self.assertEqual(top[0]["count"], 2)
