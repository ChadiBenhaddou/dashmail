import pandas as pd

from django.test import TestCase

from reports.services.data_cleaner import clean_data


class DataCleanerTest(TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "A": [1, 2, 2, None, 5],
            "B": ["x", "y", "y", "z", None],
            "C": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
        })

    def test_removes_duplicates(self):
        cleaned, log = clean_data(self.df)
        self.assertEqual(len(cleaned), 4)  # 1 duplicate removed

    def test_returns_log(self):
        cleaned, log = clean_data(self.df)
        self.assertIn("duplicates_removed", log)
