function ReportHeader({ report }) {
  const formatDate = (dateStr) => {
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
  };

  const date = formatDate(report.created_at);

  return (
    <header className="report-header" aria-label="En-tete du rapport">
      <div className="report-header-left">
        <div className="report-header-badges">
          <span className="badge badge-success">Termine</span>
          <span className="badge badge-neutral">Lien partageable</span>
          {report.month && (
            <span className="badge badge-neutral">{report.month}</span>
          )}
        </div>
        <h1 className="report-header-title">
          {report.title || "Rapport d'analyse"}
        </h1>
        <div className="report-header-meta">
          {report.source_filename && <span>{report.source_filename}</span>}
          {report.row_count != null && (
            <span>{report.row_count.toLocaleString("fr-FR")} lignes</span>
          )}
          {report.column_count != null && (
            <span>{report.column_count} colonnes</span>
          )}
          {date && <span>{date}</span>}
        </div>
      </div>
      <div className="report-header-right">
        {report.pdf_url || report.download_url ? (
          <a
            href={report.pdf_url || report.download_url}
            className="btn btn-primary btn-sm"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            PDF
          </a>
        ) : (
          <button className="btn btn-secondary btn-sm" disabled>
            PDF
          </button>
        )}
      </div>
    </header>
  );
}

export default ReportHeader;
