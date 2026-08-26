import { useParams, useLocation, Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
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
  const location = useLocation();
  const isProcessing = location.state?.processing;
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processing, setProcessing] = useState(isProcessing);
  const pollingRef = useRef(null);

  const fetchReport = () => {
    setLoading(true);
    setError(null);
    getReport(id)
      .then((data) => {
        if (data.status === 202 || (data.message && !data.report)) {
          setProcessing(true);
          setLoading(false);
        } else {
          setReport(data);
          setProcessing(false);
          setLoading(false);
          if (pollingRef.current) {
            clearInterval(pollingRef.current);
            pollingRef.current = null;
          }
        }
      })
      .catch((err) => {
        if (isProcessing) {
          setProcessing(true);
          setLoading(false);
        } else {
          setError(err);
          setLoading(false);
        }
      });
  };

  useEffect(() => {
    fetchReport();
    if (isProcessing) {
      pollingRef.current = setInterval(fetchReport, 2000);
    }
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [id]);

  if (loading && !processing) return <LoadingState />;
  if (processing && !report) return <LoadingState status="processing" />;
  if (error) return <ErrorState error={error} onRetry={fetchReport} />;

  return (
    <>
      <header className="dashboard-header" role="banner">
        <div className="dashboard-header-logo">
          <div className="dashboard-header-logo-icon" aria-hidden="true">D</div>
          <span className="dashboard-header-title">Dashboard X</span>
        </div>
        <div className="dashboard-header-right">
          <div className="dashboard-header-status">
            <span className="dashboard-header-dot" aria-hidden="true" />
            <span className="dashboard-header-status-text">Rapport prêt</span>
          </div>
          <Link to="/upload" className="btn btn-secondary btn-sm">Nouvelle analyse</Link>
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
        <p className="dashboard-footer-text">Généré automatiquement par Dashboard X</p>
        <nav className="dashboard-footer-links" aria-label="Actions du rapport">
          {report.download_url && <a href={report.download_url} download>Télécharger le fichier</a>}
          <span className="footer-sep" aria-hidden="true">·</span>
          <Link to="/upload">Nouvelle analyse</Link>
        </nav>
      </footer>
    </>
  );
}

export default DashboardPage;
