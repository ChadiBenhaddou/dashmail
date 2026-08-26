import io

from django.http import HttpResponse
from xhtml2pdf import pisa


def generate_report_pdf(report):
    charts_html = ""
    if report.charts_config:
        for chart in report.charts_config:
            data_rows = ""
            data = chart.get("data", [])
            y_key = chart.get("yAxisKey", "value")
            x_key = chart.get("xAxisKey", "label")
            for row in data:
                data_rows += "<tr><td>%s</td><td style='text-align:right;'>%s</td></tr>" % (row.get(x_key, ""), row.get(y_key, ""))
            charts_html += """
            <div style="margin-bottom:20px; page-break-inside:avoid;">
                <h3 style="color:#4F46E5; font-size:14px;">%s</h3>
                <table style="width:100%%; border-collapse:collapse; font-size:11px;">
                    <tr style="background:#F3F4F6;">
                        <th style="padding:6px 10px; text-align:left; border-bottom:1px solid #D1D5DB;">%s</th>
                        <th style="padding:6px 10px; text-align:right; border-bottom:1px solid #D1D5DB;">%s</th>
                    </tr>
                    %s
                </table>
            </div>
            """ % (chart.get("title", "Graphique"), x_key, y_key, data_rows)

    insights_html = ""
    insights = report.llm_insights
    if isinstance(insights, dict) and "insights" in insights:
        for item in insights["insights"]:
            color = {"positive": "#10B981", "negative": "#EF4444", "neutral": "#6B7280"}.get(item.get("sentiment", ""), "#6B7280")
            insights_html += """
            <div style="margin-bottom:10px; padding:8px 12px; border-left:3px solid %s; background:#F9FAFB; border-radius:4px;">
                <strong style="font-size:11px;">%s</strong>
                <p style="font-size:10px; color:#6B7280; margin:4px 0 0;">%s</p>
            </div>
            """ % (color, item.get("title", ""), item.get("description", ""))
    elif isinstance(insights, str):
        insights_html = '<p style="font-size:11px;">%s</p>' % insights

    score = report.data_quality_score or 0
    title = report.title or "Rapport d'analyse"

    html = """<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: Helvetica, Arial, sans-serif; color: #111827; margin: 20px; }
            h1 { font-size: 22px; color: #4F46E5; margin-bottom: 4px; }
            h2 { font-size: 16px; color: #374151; margin-top: 24px; border-bottom: 1px solid #E5E7EB; padding-bottom: 6px; }
            .meta { font-size: 11px; color: #6B7280; margin-bottom: 20px; }
            .badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:600; }
            .badge-green { background:#ECFDF5; color:#059669; }
            .footer { margin-top:30px; padding-top:12px; border-top:1px solid #E5E7EB; font-size:10px; color:#9CA3AF; text-align:center; }
        </style>
    </head>
    <body>
        <h1>%s</h1>
        <div class="meta">
            Statut: <span class="badge badge-green">Termin&#233;</span> &nbsp;|&nbsp;
            Lignes: %s &nbsp;|&nbsp;
            Colonnes: %s &nbsp;|&nbsp;
            Qualit&#233;: %s/100
        </div>

        <h2>Graphiques</h2>
        %s

        <h2>Analyses IA</h2>
        %s

        <div class="footer">
            G&#233;n&#233;r&#233; automatiquement par Dashbail
        </div>
    </body>
    </html>""" % (
        title,
        report.row_count or 0,
        report.column_count or 0,
        int(score),
        charts_html if charts_html else '<p style="font-size:11px; color:#9CA3AF;">Aucun graphique disponible.</p>',
        insights_html if insights_html else '<p style="font-size:11px; color:#9CA3AF;">Aucune analyse disponible.</p>',
    )

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("utf-8")), dest=result)
    if pisa_status.err:
        return None

    result.seek(0)
    return HttpResponse(
        result.getvalue(),
        content_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="rapport-%s.pdf"' % str(report.id)[:8]},
    )
