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
    "executive_summary": "string (2-4 phrases résumant l'histoire des données)",
    "overall_sentiment": "positive" | "negative" | "neutral",
    "visualizations": [
        {
            "type": "line" | "bar" | "pie" | "area" | "radar" | "scatter",
            "title": "string",
            "x_axis": "column_name",
            "y_axis": "column_name",
            "calculation": "sum" | "mean" | "count" | "max" | "min",
            "group": "column_name_or_empty",
            "description": "string explaining what this chart shows"
        }
    ],
    "kpis": [
        {
            "label": "string court",
            "x_axis": "column_name",
            "y_axis": "column_name",
            "calculation": "sum" | "mean" | "count" | "max" | "min"
        }
    ],
    "insights": [
        {
            "title": "string",
            "description": "string (2-3 phrases)",
            "sentiment": "positive" | "negative" | "neutral"
        }
    ],
    "summary": "string (3-5 phrases de résumé général)",
    "custom_visualizations": [
        {
            "type": "line" | "bar" | "pie" | "area" | "radar" | "scatter",
            "title": "string",
            "x_axis": "column_name",
            "y_axis": "column_name",
            "calculation": "sum" | "mean" | "count" | "max" | "min",
            "group": "column_name_or_empty",
            "description": "string"
        }
    ]
}

Règles :
- Ne génère JAMAIS de nombres — utilise uniquement les noms de colonnes pour que pandas calcule.
- Choisis 4 à 7 visualisations dans "visualizations" (analyse automatique pertinente), en
  mélangeant les types pour un tableau de bord riche : tendance (line/area), comparaison
  (bar), répartition (pie), performance/coverage (radar), corrélation (scatter).
- Utilise au maximum UNE fois le type "pie".
- Pour "radar", choisis une colonne catégorielle en x_axis et une mesure numérique en y_axis.
- Pour "scatter", choisis deux colonnes numériques en x_axis et y_axis (sans calculation).
- Optionnel : pour line/bar/area tu peux fournir "group" (une colonne catégorielle) pour créer
  une série multiple (une ligne/barre par valeur du groupe). Mets "group" à "" si non souhaité.
- Dans "kpis", fournis 4 indicateurs clés. Utilise uniquement des noms de colonnes.
- Si l'utilisateur a formulé une demande spécifique, traduis ses demandes de graphiques et
  de calculs dans le tableau "custom_visualizations" (en PLUS des visualizations automatiques).
  Pour chaque demande, précise le calcul souhaité (somme, moyenne, comptage, max, min) via
  le champ "calculation". Ne renvoie que des colonnes qui existent dans les données.
- Si l'utilisateur n'a formulé aucune demande spécifique, "custom_visualizations" doit être un tableau vide [].
- Les insights doivent être rédigés en français clair et non technique.
- Chaque insight doit comporter un sentiment (positive/negative/neutral).
- "executive_summary" doit être un résumé impactant, en français, orienté décision.
- Retourne UNIQUEMENT le JSON, sans texte additionnel.
""".strip()


def build_analysis_prompt(column_summary, custom_prompt=""):
    summary_json = json.dumps(column_summary, ensure_ascii=False, indent=2)
    user_prompt = (
        "Voici le résumé structuré du jeu de données :\n\n"
        f"```json\n{summary_json}\n```\n\n"
        "Propose les visualisations et insights pertinents pour ce jeu de données."
    )
    if custom_prompt and custom_prompt.strip():
        user_prompt += (
            "\n\nDemande spécifique de l'utilisateur (à respecter) :\n"
            f"{custom_prompt.strip()}\n"
        )
    full_system = f"{SYSTEM_PROMPT}\n\n{SCHEMA_INSTRUCTIONS}"
    return full_system, user_prompt
