function DataQuality({ score, cleaningLog }) {
  const color =
    score >= 80
      ? "var(--c-green)"
      : score >= 50
      ? "var(--c-ember)"
      : "var(--c-red)";

  const log = cleaningLog && typeof cleaningLog === "object" ? cleaningLog : {};

  const items = [
    {
      label: "Doublons supprimes",
      value: log.duplicates_removed,
    },
    {
      label: "Colonnes supprimees",
      value: Array.isArray(log.columns_dropped)
        ? log.columns_dropped.length
        : null,
    },
    {
      label: "Valeurs manquantes imputees",
      value: countMap(log.nulls_imputed),
    },
    {
      label: "Dates normalisees",
      value: Array.isArray(log.date_normalized) ? log.date_normalized.length : null,
    },
    {
      label: "Colonnes texte nettoyees",
      value: Array.isArray(log.strings_cleaned) ? log.strings_cleaned.length : null,
    },
    {
      label: "Lignes supprimees",
      value: log.rows_dropped_nulls,
    },
  ];

  const renderable = items.filter((i) => i.value != null);

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
        <span className="dq-label">{score >= 80 ? "Excellent" : score >= 50 ? "Correct" : "Faible"}</span>
      </div>
      {renderable.length > 0 && (
        <ul className="dq-log-list">
          {renderable.map((item) => (
            <li key={item.label} className="dq-log-item">
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function countMap(obj) {
  if (!obj || typeof obj !== "object" || Array.isArray(obj)) return null;
  return Object.keys(obj).length;
}

export default DataQuality;
