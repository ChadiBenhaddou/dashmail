function DataQuality({ score, label, badge, description }) {
  return (
    <div className="card data-quality" role="figure" aria-label={`Qualité des données: ${score} pour cent`}>
      <div className="dq-score" aria-hidden="true">{score}</div>
      <div className="dq-bar-wrap" role="progressbar" aria-valuenow={score} aria-valuemin={0} aria-valuemax={100} aria-label={`Score de qualité: ${score}%`}>
        <div className="dq-bar" style={{ width: `${score}%` }} />
      </div>
      <div className="dq-row">
        <span className="dq-label">{label || "Excellent"}</span>
        {badge && <span className="badge badge-success">{badge}</span>}
      </div>
      {description && <p className="dq-desc">{description}</p>}
    </div>
  );
}

export default DataQuality;
