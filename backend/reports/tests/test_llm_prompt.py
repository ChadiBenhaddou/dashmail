from django.test import TestCase

from reports.services.llm_prompt import build_analysis_prompt


class LLMPromptTest(TestCase):
    def test_build_prompt(self):
        summary = {
            "columns": [
                {"name": "Ventes", "dtype": "int64"},
                {"name": "Region", "dtype": "object"},
            ],
            "row_count": 100,
            "numeric_columns": ["Ventes"],
            "categorical_columns": ["Region"],
        }
        system_prompt, user_prompt = build_analysis_prompt(summary)
        self.assertIn("Ventes", user_prompt)
        self.assertIn("JSON", system_prompt)

    def test_custom_prompt_is_included(self):
        summary = {"columns": [{"name": "Ventes", "dtype": "int64"}]}
        _, user_prompt = build_analysis_prompt(
            summary, "Fais un camembert par region"
        )
        self.assertIn("Fais un camembert par region", user_prompt)
        self.assertIn("Demande spécifique", user_prompt)

    def test_custom_prompt_blank_not_included(self):
        summary = {"columns": [{"name": "Ventes", "dtype": "int64"}]}
        _, user_prompt = build_analysis_prompt(summary, "")
        self.assertNotIn("Demande spécifique", user_prompt)

    def test_schema_mentions_custom_visualizations(self):
        summary = {"columns": [{"name": "Ventes", "dtype": "int64"}]}
        system_prompt, _ = build_analysis_prompt(summary)
        self.assertIn("custom_visualizations", system_prompt)
        self.assertIn("calculation", system_prompt)

    def test_schema_mentions_dashboard_fields(self):
        summary = {"columns": [{"name": "Ventes", "dtype": "int64"}]}
        system_prompt, _ = build_analysis_prompt(summary)
        self.assertIn("executive_summary", system_prompt)
        self.assertIn("overall_sentiment", system_prompt)
        self.assertIn("kpis", system_prompt)
        self.assertIn("radar", system_prompt)
        self.assertIn("scatter", system_prompt)
        self.assertIn("area", system_prompt)
        self.assertIn("group", system_prompt)
