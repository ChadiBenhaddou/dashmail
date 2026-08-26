import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { getReport } from "../services/api.js";
import LoadingState from "../components/LoadingState.jsx";
import ErrorState from "../components/ErrorState.jsx";
import ReportHeader from "../components/ReportHeader.jsx";
import KPICard from "../components/KPICard.jsx";
import ChartRenderer from "../components/ChartRenderer.jsx";
import InsightList from "../components/InsightList.jsx";
import DataQuality from "../components/DataQuality.jsx";

function DashboardPage() {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchReport = () => {
    setLoading(true);
    setError(null);
    getReport(id)
      .then(setReport)
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReport();
  }, [id]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState error={error} onRetry={fetchReport} />;

  return (
    <>
      <header className="dashboard-header" role="banner">
        <div className="dashboard-header-logo">
          <div className="dashboard-header-logo-icon" aria-hidden="true">D</div>
          <span className="dashboard-header-title">Dashboard</span>
        </div>
        <div className="dashboard-header-status">
          <span className="dashboard-header-dot" aria-hidden="true" />
          <span className="dashboard-header-status-text">Rapport prêt</span>
        </div>
      </header>

      <main className="dashboard" role="main">
        <ReportHeader report={report} />

        <section className="kpi-grid" aria-label="Indicateurs clés">
          {report.kpis?.map((kpi, i) => (
            <KPICard key={i} {...kpi} />
          ))}
        </section>

        <section className="charts-grid" aria-label="Graphiques">
          {report.charts?.map((chart, i) => (
            <div key={i} className="card">
              <ChartRenderer {...chart} />
            </div>
          ))}
        </section>

        <section className="bottom-grid" aria-label="Analyses et qualité">
          {report.insights && <InsightList insights={report.insights} />}
          {report.data_quality && <DataQuality {...report.data_quality} />}
        </section>
      </main>

      <footer className="dashboard-footer" role="contentinfo">
        <p className="dashboard-footer-text">Généré automatiquement par Dashbail</p>
        <nav className="dashboard-footer-links" aria-label="Actions du rapport">
          <a href={report.download_url} download>Télécharger le PDF</a>
          <span className="footer-sep" aria-hidden="true">·</span>
          <a href={report.download_url} download>Exporter</a>
          <span className="footer-sep" aria-hidden="true">·</span>
          <a href="/">Nouvelle analyse</a>
        </nav>
      </footer>
    </>
  );
}

export default DashboardPage;
