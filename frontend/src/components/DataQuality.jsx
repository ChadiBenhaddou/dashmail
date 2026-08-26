function DataQuality({ score, label, badge, description }) {
  const color =
    score >= 80
      ? "var(--c-green)"
      : score >= 50
      ? "var(--c-ember)"
      : "var(--c-red)";

  return (
    <div className="card dq-card" role="figure" aria-label={`Qualite: ${score}%`}>
      <div className="dq-score">{score}</div>
      <div className="dq-bar">
        <div
          className="dq-bar-fill"
          style={{ width: `${score}%`, background: color }}
        />
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <span className="dq-label">{label || "Excellent"}</span>
        {badge && <span className="badge badge-success">{badge}</span>}
      </div>
      {description && (
        <p className="dq-log" style={{ marginTop: "10px" }}>
          {description}
        </p>
      )}
    </div>
  );
}

export default DataQuality;
