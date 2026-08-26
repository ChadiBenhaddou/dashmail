import json


SYSTEM_PROMPT = (
    "Tu es un expert en analyse de données. Tu reçois le résumé structuré "
    "d'un jeu de données CSV/Excel. Tu dois proposer les visualisations les "
    "plus pertinentes et rédiger un résumé d'insights clairs en français. "
    "Tu ne génères JAMAIS de chiffres — les données chiffrées proviennent "
    "uniquement de pandas."
)

SCHEMA_INSTRUCTIONS = """
Tu dois retourner un JSON strict avec la structure suivante :

{
    "visualizations": [
        {
            "type": "line" | "bar" | "pie",
            "title": "string",
            "x_axis": "column_name",
            "y_axis": "column_name",
            "description": "string explaining what this chart shows"
        }
    ],
    "insights": [
        {
            "title": "string",
            "description": "string (2-3 phrases)",
            "sentiment": "positive" | "negative" | "neutral"
        }
    ],
    "summary": "string (3-5 phrases de résumé général)"
}

Règles :
- Ne génère JAMAIS de nombres — utilise uniquement les noms de colonnes pour que pandas calcule.
- Choisis 3 à 5 visualisations les plus pertinentes.
- Les insights doivent être rédigés en français clair et non technique.
- Chaque insight doit comporter un sentiment (positive/negative/neutral).
- Retourne UNIQUEMENT le JSON, sans texte additionnel.
""".strip()


def build_analysis_prompt(column_summary):
    summary_json = json.dumps(column_summary, ensure_ascii=False, indent=2)
    user_prompt = (
        "Voici le résumé structuré du jeu de données :\n\n"
        f"```json\n{summary_json}\n```\n\n"
        "Propose les visualisations et insights pertinents pour ce jeu de données."
    )
    return SYSTEM_PROMPT, user_prompt
