function InsightList({ insights }) {
  return (
    <div className="card insight-list" aria-label="Insights de l'analyse IA">
      <div className="insight-header">
        <span className="badge badge-ai">Analyse IA</span>
      </div>
      <ol className="insights-ol">
        {insights.map((insight, i) => (
          <li key={i} className={`insight-item ${insight.sentiment === "negative" ? "insight-negative" : ""}`}>
            <span className={`insight-number ${insight.sentiment === "negative" ? "number-negative" : "number-positive"}`} aria-hidden="true">
              {String(i + 1).padStart(2, "0")}
            </span>
            <div>
              <h4 className="insight-title">{insight.title}</h4>
              <p className="insight-desc">{insight.description}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}

export default InsightList;
