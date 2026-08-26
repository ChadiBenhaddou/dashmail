function formatDate(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  if (Number.isNaN(d.getTime())) return null;
  return d.toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatFileSize(size) {
  if (!size) return null;
  if (typeof size === "string") return size;
  if (size < 1024) return `${size} o`;
  if (size < 1048576) return `${(size / 1024).toFixed(1)} Ko`;
  return `${(size / 1048576).toFixed(1)} Mo`;
}

function ReportHeader({ report }) {
  const date = formatDate(report.created_at);
  const fileSize = formatFileSize(report.file_size);

  return (
    <header className="card report-header" aria-label="En-tête du rapport">
      <div className="rh-badges">
        <span className="badge badge-success">Analyse terminée</span>
        <span className="badge badge-neutral">Rapport partagé · Accès sans compte</span>
        {report.month && <span className="badge badge-neutral">{report.month}</span>}
      </div>

      <h1 className="rh-title">{report.title || "Rapport d'analyse"}</h1>

      <div className="rh-meta">
        {report.source_filename && (
          <span className="rh-meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <span className="rh-source">{report.source_filename}</span>
          </span>
        )}
        {report.row_count != null && (
          <span className="rh-meta-item">
            {report.row_count.toLocaleString("fr-FR")} lignes
          </span>
        )}
        {report.column_count != null && (
          <span className="rh-meta-item">
            {report.column_count} colonnes
          </span>
        )}
        {date && (
          <span className="rh-meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            {date}
          </span>
        )}
      </div>

      <div className="rh-actions">
        {report.download_url ? (
          <a href={report.download_url} className="btn-primary" download aria-label="Télécharger le rapport">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            Télécharger
            {fileSize && <span className="rh-size">({fileSize})</span>}
          </a>
        ) : (
          <button className="btn-primary" disabled aria-label="Téléchargement non disponible">
            Télécharger
          </button>
        )}
      </div>

      <p className="rh-note">Ce lien sécurisé expire dans 7 jours. Enregistrez le rapport pour y accéder ultérieurement.</p>
    </header>
  );
}

export default ReportHeader;
