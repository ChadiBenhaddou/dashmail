import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getReports } from "../services/api.js";

const STATUS = {
  completed: { label: "Termine", cls: "badge-success" },
  processing: { label: "En cours", cls: "badge-primary" },
  pending: { label: "En attente", cls: "badge-info" },
  failed: { label: "Echoue", cls: "badge-error" },
  cleaning: { label: "Nettoyage", cls: "badge-primary" },
  analyzing: { label: "Analyse IA", cls: "badge-ai" },
};

export default function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    getReports()
      .then((data) => setReports(data.results || data))
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  const filtered = reports.filter((r) => {
    const matchSearch =
      !search || r.title?.toLowerCase().includes(search.toLowerCase());
    const matchFilter = filter === "all" || r.status === filter;
    return matchSearch && matchFilter;
  });

  if (loading)
    return (
      <div className="upload-page">
        <div className="loading-spinner" />
      </div>
    );
  if (error)
    return (
      <div className="upload-page">
        <div className="auth-error">{error.message}</div>
      </div>
    );

  return (
    <div className="reports-page">
      <div className="reports-container">
        <div className="reports-header">
          <div>
            <h1 className="reports-title">Mes rapports</h1>
            <p className="reports-subtitle">
              {reports.length} rapport{reports.length !== 1 ? "s" : ""}
            </p>
          </div>
          <Link to="/upload" className="btn btn-accent btn-sm">
            + Nouveau
          </Link>
        </div>

        <div className="reports-filters">
          <input
            type="text"
            placeholder="Rechercher..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="reports-search"
          />
          <div className="reports-filter-pills">
            {["all", "completed", "processing", "failed"].map((f) => (
              <button
                key={f}
                className={`filter-pill ${filter === f ? "filter-pill-active" : ""}`}
                onClick={() => setFilter(f)}
              >
                {f === "all" ? "Tous" : STATUS[f]?.label || f}
              </button>
            ))}
          </div>
        </div>

        {filtered.length === 0 ? (
          <div className="reports-empty">
            <p>Aucun rapport pour l'instant.</p>
            <Link to="/upload" className="btn btn-primary btn-sm">
              Analyser un fichier
            </Link>
          </div>
        ) : (
          <div className="reports-list">
            {filtered.map((report) => {
              const st = STATUS[report.status] || {
                label: report.status,
                cls: "badge-neutral",
              };
              return (
                <Link
                  key={report.id}
                  to={`/dashboard/${report.dashboard_link}`}
                  className="report-card"
                >
                  <div className="report-card-header">
                    <h3 className="report-card-title">{report.title}</h3>
                    <span className={`badge ${st.cls}`}>{st.label}</span>
                  </div>
                  <div className="report-card-meta">
                    {report.row_count && (
                      <span>{report.row_count.toLocaleString()} lignes</span>
                    )}
                    {report.column_count && (
                      <span>{report.column_count} colonnes</span>
                    )}
                    {report.file_size && (
                      <span>{(report.file_size / 1024).toFixed(0)} Ko</span>
                    )}
                  </div>
                  <div className="report-card-date">
                    {new Date(report.created_at).toLocaleDateString("fr-FR", {
                      day: "numeric",
                      month: "short",
                      year: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
