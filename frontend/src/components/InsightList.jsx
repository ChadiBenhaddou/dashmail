function InsightList({ insights }) {
  return (
    <div className="card" style={{ padding: "20px" }} aria-label="Insights IA">
      <div style={{ marginBottom: "14px" }}>
        <span className="badge badge-ai">Analyse IA</span>
      </div>
      <ul className="insight-list">
        {insights.map((insight, i) => (
          <li
            key={i}
            className={`insight-item ${insight.sentiment === "negative" ? "negative" : "positive"}`}
          >
            <span className="insight-num">
              {String(i + 1).padStart(2, "0")}
            </span>
            <div>
              <h4 className="insight-title">{insight.title}</h4>
              <p className="insight-desc">{insight.description}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default InsightList;
