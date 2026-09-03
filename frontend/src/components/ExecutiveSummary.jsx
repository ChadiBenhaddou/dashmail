function ExecutiveSummary({ summary, sentiment }) {
  const labelMap = {
    positive: "Perspectives positives",
    negative: "Point de vigilance",
    neutral: "Analyse neutre",
  };
  const cls = sentiment === "positive" ? "positive" : sentiment === "negative" ? "negative" : "neutral";

  if (!summary && !sentiment) return null;
  if (!summary) return null;

  return (
    <section className="card summary-banner" aria-label="Synthèse exécutive">
      <div className="summary-banner-top">
        <span className="badge badge-ai">Synthèse IA</span>
        {sentiment && (
          <span className={`sentiment-badge ${cls}`}>{labelMap[sentiment] || sentiment}</span>
        )}
      </div>
      <p className="summary-banner-text">{summary}</p>
    </section>
  );
}

export default ExecutiveSummary;
