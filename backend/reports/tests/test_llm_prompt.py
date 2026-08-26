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
