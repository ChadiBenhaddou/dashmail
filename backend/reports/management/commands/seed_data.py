from django.core.management.base import BaseCommand

from reports.models import Report


class Command(BaseCommand):
    help = "Create sample Report objects for development"

    def handle(self, *args, **options):
        reports_data = [
            {
                "title": "Ventes Q1 2024",
                "sender_email": "ventes@example.com",
                "row_count": 1250,
                "column_count": 8,
                "file_size": 524288,
                "data_quality_score": 92,
                "llm_insights": {
                    "insights": [
                        {
                            "title": "Croissance du revenu",
                            "description": "Le revenu a augment\u00e9 de 15% par rapport au T4 2023, port\u00e9 par une forte demande en \u00e9lectronique.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Meilleure r\u00e9tention client",
                            "description": "Le taux de r\u00e9tention client a atteint 78%, en hausse de 5 points par rapport au trimestre pr\u00e9c\u00e9dent.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Performance r\u00e9gionale",
                            "description": "La corridor Nord-Ouest affiche la croissance la plus forte, tandis que le Sud reste en retard.",
                            "sentiment": "neutral",
                        },
                    ],
                    "summary": "Trimestre solide avec croissance \u00e0 deux chiffres et am\u00e9lioration de la r\u00e9tention. \u00c9lectronique reste le moteur principal.",
                },
                "charts_config": [
                    {
                        "type": "line",
                        "title": "Revenu mensuel",
                        "xAxisKey": "month",
                        "yAxisKey": "revenue",
                        "data": [
                            {"month": "Jan", "revenue": 42000},
                            {"month": "F\u00e9v", "revenue": 48500},
                            {"month": "Mar", "revenue": 51200},
                        ],
                    },
                    {
                        "type": "bar",
                        "title": "Ventes par r\u00e9gion",
                        "xAxisKey": "region",
                        "yAxisKey": "sales",
                        "data": [
                            {"region": "Nord", "sales": 320},
                            {"region": "Sud", "sales": 280},
                            {"region": "Est", "sales": 195},
                            {"region": "Ouest", "sales": 455},
                        ],
                    },
                ],
                "cleaning_log": {
                    "duplicates_removed": 12,
                    "nulls_filled": 34,
                    "columns_dropped": [],
                },
            },
            {
                "title": "Rapport Marketing Mars",
                "sender_email": "marketing@example.com",
                "row_count": 3200,
                "column_count": 12,
                "file_size": 1048576,
                "data_quality_score": 87,
                "llm_insights": {
                    "insights": [
                        {
                            "title": "ROI des campagnes \u00e9lev\u00e9",
                            "description": "Le ROI moyen a atteint 3.2x sur l'ensemble des canaux, d\u00e9passant l'objectif de 2.5x.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Croissance r\u00e9seaux sociaux",
                            "description": "Les impressions sur les r\u00e9seaux sociaux ont augment\u00e9 de 28% mois par mois.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Recommandation budg\u00e9taire",
                            "description": "Rediriger 15% du budget print vers le digital pour optimiser le ROI.",
                            "sentiment": "neutral",
                        },
                    ],
                    "summary": "Campagnes performantes avec ROI de 3.2x. Les r\u00e9seaux sociaux sont le canal \u00e0 fort potentiel.",
                },
                "charts_config": [
                    {
                        "type": "bar",
                        "title": "Performance par canal",
                        "xAxisKey": "channel",
                        "yAxisKey": "conversions",
                        "data": [
                            {"channel": "Email", "conversions": 890},
                            {"channel": "Social", "conversions": 1240},
                            {"channel": "Search", "conversions": 670},
                            {"channel": "Display", "conversions": 320},
                        ],
                    },
                    {
                        "type": "line",
                        "title": "Impressions hebdomadaires",
                        "xAxisKey": "week",
                        "yAxisKey": "impressions",
                        "data": [
                            {"week": "S1", "impressions": 45000},
                            {"week": "S2", "impressions": 52000},
                            {"week": "S3", "impressions": 48500},
                            {"week": "S4", "impressions": 61000},
                        ],
                    },
                ],
                "cleaning_log": {
                    "duplicates_removed": 45,
                    "nulls_filled": 112,
                    "columns_dropped": ["internal_notes"],
                },
            },
            {
                "title": "Analyse RH - Effectifs 2024",
                "sender_email": "rh@example.com",
                "row_count": 480,
                "column_count": 15,
                "file_size": 262144,
                "data_quality_score": 95,
                "llm_insights": {
                    "insights": [
                        {
                            "title": "Effectifs stables",
                            "description": "L'effectif total est de 480 employ\u00e9s avec une anciennet\u00e9 moyenne de 3.4 ans.",
                            "sentiment": "neutral",
                        },
                        {
                            "title": "Turnover ma\u00eetris\u00e9",
                            "description": "Le taux de turnover volontaire est de 12%, bien en dessous de la moyenne du secteur (18%).",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Croissance ing\u00e9nierie",
                            "description": "Le d\u00e9partement ing\u00e9nierie affiche la plus forte croissance \u00e0 +22% annuel.",
                            "sentiment": "positive",
                        },
                    ],
                    "summary": "Ressources humaines en bonne sant\u00e9. Turnover bas, croissance forte en ing\u00e9nierie.",
                },
                "charts_config": [
                    {
                        "type": "bar",
                        "title": "Effectifs par d\u00e9partement",
                        "xAxisKey": "department",
                        "yAxisKey": "count",
                        "data": [
                            {"department": "Ing\u00e9nierie", "count": 180},
                            {"department": "Ventes", "count": 95},
                            {"department": "Marketing", "count": 65},
                            {"department": "RH", "count": 30},
                            {"department": "Finance", "count": 45},
                            {"department": "Ops", "count": 65},
                        ],
                    },
                ],
                "cleaning_log": {
                    "duplicates_removed": 3,
                    "nulls_filled": 18,
                    "columns_dropped": ["comments"],
                },
            },
            {
                "title": "Performance Financi\u00e8re 2024",
                "sender_email": "finance@example.com",
                "row_count": 890,
                "column_count": 10,
                "file_size": 786432,
                "data_quality_score": 98,
                "llm_insights": {
                    "insights": [
                        {
                            "title": "Marge nette en hausse",
                            "description": "La marge nette a atteint 14.2%, en hausse par rapport aux 11.8% de 2023.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "R\u00e9duction des charges",
                            "description": "Les d\u00e9penses d'exploitation ont \u00e9t\u00e9 r\u00e9duites de 8% gr\u00e2ce aux initiatives d'automatisation.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Tr\u00e9sorerie solide",
                            "description": "Le flux de tr\u00e9sorerie op\u00e9rationnel a atteint 2.4M$ avec des d\u00e9lais d'encaissements r\u00e9duits.",
                            "sentiment": "positive",
                        },
                    ],
                    "summary": "Exercice financier excellent avec am\u00e9lioration de la marge et r\u00e9duction des charges op\u00e9rationnelles.",
                },
                "charts_config": [
                    {
                        "type": "line",
                        "title": "Revenus vs D\u00e9penses trimestriels",
                        "xAxisKey": "quarter",
                        "yAxisKey": "revenue",
                        "data": [
                            {"quarter": "T1", "revenue": 1200000, "expenses": 980000},
                            {"quarter": "T2", "revenue": 1350000, "expenses": 1020000},
                            {"quarter": "T3", "revenue": 1480000, "expenses": 1050000},
                            {"quarter": "T4", "revenue": 1620000, "expenses": 1100000},
                        ],
                    },
                ],
                "cleaning_log": {
                    "duplicates_removed": 0,
                    "nulls_filled": 8,
                    "columns_dropped": [],
                },
            },
            {
                "title": "Satisfaction Client T3",
                "sender_email": "support@example.com",
                "row_count": 2100,
                "column_count": 6,
                "file_size": 393216,
                "data_quality_score": 89,
                "llm_insights": {
                    "insights": [
                        {
                            "title": "Score de satisfaction \u00e9lev\u00e9",
                            "description": "Le score de satisfaction client est de 4.3/5.0, en hausse par rapport au T2.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "NPS en progression",
                            "description": "Le NPS a augment\u00e9 \u00e0 +42, en hausse par rapport \u00e0 +35 au T2.",
                            "sentiment": "positive",
                        },
                        {
                            "title": "Retards de livraison",
                            "description": "Les retards de livraison repr\u00e9sentent 31% des tickets, \u00e0 am\u00e9liorer.",
                            "sentiment": "negative",
                        },
                    ],
                    "summary": "Satisfaction client globalement bonne avec NPS en progression. Les retards de livraison restent le point d'am\u00e9lioration principal.",
                },
                "charts_config": [
                    {
                        "type": "bar",
                        "title": "Satisfaction par cat\u00e9gorie",
                        "xAxisKey": "category",
                        "yAxisKey": "score",
                        "data": [
                            {"category": "Produit", "score": 4.5},
                            {"category": "Support", "score": 4.2},
                            {"category": "Livraison", "score": 3.8},
                            {"category": "Prix", "score": 4.1},
                        ],
                    },
                    {
                        "type": "line",
                        "title": "Tendance NPS",
                        "xAxisKey": "month",
                        "yAxisKey": "nps",
                        "data": [
                            {"month": "Jul", "nps": 35},
                            {"month": "Ao\u00fb", "nps": 38},
                            {"month": "Sep", "nps": 42},
                        ],
                    },
                ],
                "cleaning_log": {
                    "duplicates_removed": 22,
                    "nulls_filled": 56,
                    "columns_dropped": ["agent_name"],
                },
            },
        ]

        created_count = 0
        for data in reports_data:
            _, created = Report.objects.get_or_create(
                title=data["title"],
                defaults={
                    **data,
                    "status": Report.Status.COMPLETED,
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created report: {data['title']}"))
            else:
                self.stdout.write(f"Report already exists: {data['title']}")

        self.stdout.write(
            self.style.SUCCESS(f"\nSeed complete: {created_count} reports created")
        )
