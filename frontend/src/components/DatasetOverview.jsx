function DatasetOverview({ profile }) {
  if (!profile || Object.keys(profile).length === 0) return null;

  const { numeric_columns = [], categorical_columns = [], date_columns = [], row_count, column_count, missing_total } = profile;

  const fmt = (v) => {
    if (v == null) return "—";
    if (typeof v === "number") return v.toLocaleString("fr-FR", { maximumFractionDigits: 1 });
    return String(v);
  };

  return (
    <section className="card overview-card" aria-label="Aperçu du jeu de données">
      <div className="overview-header">
        <span className="badge badge-ai">Profil du jeu de données</span>
      </div>

      <div className="overview-stats">
        <div className="overview-stat">
          <span className="overview-stat-value">{fmt(row_count)}</span>
          <span className="overview-stat-label">lignes</span>
        </div>
        <div className="overview-stat">
          <span className="overview-stat-value">{fmt(column_count)}</span>
          <span className="overview-stat-label">colonnes</span>
        </div>
        <div className="overview-stat">
          <span className="overview-stat-value">{fmt(missing_total)}</span>
          <span className="overview-stat-label">valeurs manquantes</span>
        </div>
        <div className="overview-stat">
          <span className="overview-stat-value">{date_columns.length}</span>
          <span className="overview-stat-label">colonnes date</span>
        </div>
      </div>

      {numeric_columns.length > 0 && (
        <div className="overview-table-wrap">
          <table className="overview-table">
            <thead>
              <tr>
                <th>Colonne</th>
                <th>Min</th>
                <th>Max</th>
                <th>Moyenne</th>
                <th>Somme</th>
              </tr>
            </thead>
            <tbody>
              {numeric_columns.map((c) => (
                <tr key={c.name}>
                  <td className="overview-colname">{c.name}</td>
                  <td>{fmt(c.min)}</td>
                  <td>{fmt(c.max)}</td>
                  <td>{fmt(c.mean)}</td>
                  <td>{fmt(c.sum)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {categorical_columns.length > 0 && (
        <div className="overview-cats">
          {categorical_columns.map((c) => (
            <div key={c.name} className="overview-cat">
              <span className="overview-cat-name">{c.name}</span>
              <div className="overview-cat-top">
                {(c.top_values || []).map((tv) => (
                  <span key={tv.value} className="chip">
                    {tv.value} <strong>{fmt(tv.count)}</strong>
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default DatasetOverview;
