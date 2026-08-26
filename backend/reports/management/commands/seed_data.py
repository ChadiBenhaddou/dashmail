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
                "data_quality_score": 0.92,
                "llm_insights": (
                    "Revenue increased by 15% compared to Q4 2023. "
                    "The top-performing product category was Electronics "
                    "with 340 units sold. Customer retention rate improved "
                    "to 78%. Regional performance shows strongest growth "
                    "in the North-West corridor."
                ),
                "charts_config": [
                    {
                        "type": "line",
                        "title": "Monthly Revenue Trend",
                        "dataKey": "revenue",
                        "xAxis": "month",
                        "data": [
                            {"month": "Jan", "revenue": 42000},
                            {"month": "Feb", "revenue": 48500},
                            {"month": "Mar", "revenue": 51200},
                        ],
                    },
                    {
                        "type": "bar",
                        "title": "Sales by Region",
                        "dataKey": "sales",
                        "xAxis": "region",
                        "data": [
                            {"region": "North", "sales": 320},
                            {"region": "South", "sales": 280},
                            {"region": "East", "sales": 195},
                            {"region": "West", "sales": 455},
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
                "data_quality_score": 0.87,
                "llm_insights": (
                    "Campaign ROI reached 3.2x across all channels. "
                    "Social media impressions grew by 28% month-over-month. "
                    "Email open rates averaged 22.5%, above industry benchmark. "
                    "Recommended shift 15% of print budget to digital channels."
                ),
                "charts_config": [
                    {
                        "type": "bar",
                        "title": "Campaign Performance by Channel",
                        "dataKey": "conversions",
                        "xAxis": "channel",
                        "data": [
                            {"channel": "Email", "conversions": 890},
                            {"channel": "Social", "conversions": 1240},
                            {"channel": "Search", "conversions": 670},
                            {"channel": "Display", "conversions": 320},
                        ],
                    },
                    {
                        "type": "line",
                        "title": "Weekly Impressions",
                        "dataKey": "impressions",
                        "xAxis": "week",
                        "data": [
                            {"week": "W1", "impressions": 45000},
                            {"week": "W2", "impressions": 52000},
                            {"week": "W3", "impressions": 48500},
                            {"week": "W4", "impressions": 61000},
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
                "data_quality_score": 0.95,
                "llm_insights": (
                    "Total headcount stands at 480 employees. Average "
                    "tenure is 3.4 years. Voluntary attrition rate is "
                    "12%, below industry average of 18%. Engineering "
                    "department has the highest growth at 22% YoY. "
                    "Average training hours per employee: 24h."
                ),
                "charts_config": [
                    {
                        "type": "bar",
                        "title": "Headcount by Department",
                        "dataKey": "count",
                        "xAxis": "department",
                        "data": [
                            {"department": "Engineering", "count": 180},
                            {"department": "Sales", "count": 95},
                            {"department": "Marketing", "count": 65},
                            {"department": "HR", "count": 30},
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
                "title": "Performance Financiere 2024",
                "sender_email": "finance@example.com",
                "row_count": 890,
                "column_count": 10,
                "file_size": 786432,
                "data_quality_score": 0.98,
                "llm_insights": (
                    "Net profit margin improved to 14.2%, up from 11.8% "
                    "in 2023. Operating expenses reduced by 8% through "
                    "automation initiatives. Cash flow from operations "
                    "reached $2.4M. Accounts receivable days decreased "
                    "from 45 to 38 days."
                ),
                "charts_config": [
                    {
                        "type": "line",
                        "title": "Quarterly Revenue vs Expenses",
                        "dataKey": "revenue",
                        "xAxis": "quarter",
                        "data": [
                            {"quarter": "Q1", "revenue": 1200000, "expenses": 980000},
                            {"quarter": "Q2", "revenue": 1350000, "expenses": 1020000},
                            {"quarter": "Q3", "revenue": 1480000, "expenses": 1050000},
                            {"quarter": "Q4", "revenue": 1620000, "expenses": 1100000},
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
                "data_quality_score": 0.89,
                "llm_insights": (
                    "Overall customer satisfaction score: 4.3/5.0. "
                    "NPS score increased to +42, up from +35 in Q2. "
                    "Top complaint category: delivery delays (31% of tickets). "
                    "Live chat adoption grew by 40%. First response time "
                    "averaged 2.1 hours, meeting the SLA target."
                ),
                "charts_config": [
                    {
                        "type": "bar",
                        "title": "Satisfaction by Category",
                        "dataKey": "score",
                        "xAxis": "category",
                        "data": [
                            {"category": "Product", "score": 4.5},
                            {"category": "Support", "score": 4.2},
                            {"category": "Delivery", "score": 3.8},
                            {"category": "Pricing", "score": 4.1},
                        ],
                    },
                    {
                        "type": "line",
                        "title": "NPS Trend",
                        "dataKey": "nps",
                        "xAxis": "month",
                        "data": [
                            {"month": "Jul", "nps": 35},
                            {"month": "Aug", "nps": 38},
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
