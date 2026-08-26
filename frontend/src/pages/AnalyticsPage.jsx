import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getStats } from "../services/api.js";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = { completed: "#10B981", processing: "#4F46E5", failed: "#EF4444", pending: "#9CA3AF" };

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStats()
      .then(setStats)
      .catch(() => setStats({ total: 0, completed: 0, failed: 0, processing: 0, total_size_bytes: 0, recent_reports: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="auth-page"><div className="loading-spinner" /></div>;
  if (!stats) return null;

  const pieData = [
    { name: "Terminés", value: stats.completed, color: COLORS.completed },
    { name: "En cours", value: stats.processing, color: COLORS.processing },
    { name: "Échoués", value: stats.failed, color: COLORS.failed },
  ].filter((d) => d.value > 0);

  const barData = stats.recent_reports.map((r) => ({
    name: r.title?.substring(0, 12) || "Sans titre",
    lignes: r.row_count || 0,
  }));

  return (
    <div className="analytics-page">
      <div className="analytics-container">
        <div className="reports-header">
          <div>
            <h1 className="reports-title">Analytics</h1>
            <p className="reports-subtitle">Vue d'ensemble de votre utilisation</p>
          </div>
        </div>

        <div className="analytics-kpi-grid">
          <div className="analytics-kpi">
            <span className="analytics-kpi-value">{stats.total}</span>
            <span className="analytics-kpi-label">Total rapports</span>
          </div>
          <div className="analytics-kpi analytics-kpi-success">
            <span className="analytics-kpi-value">{stats.completed}</span>
            <span className="analytics-kpi-label">Terminés</span>
          </div>
          <div className="analytics-kpi analytics-kpi-error">
            <span className="analytics-kpi-value">{stats.failed}</span>
            <span className="analytics-kpi-label">Échoués</span>
          </div>
          <div className="analytics-kpi analytics-kpi-primary">
            <span className="analytics-kpi-value">{(stats.total_size_bytes / (1024 * 1024)).toFixed(1)} Mo</span>
            <span className="analytics-kpi-label">Données traitées</span>
          </div>
        </div>

        <div className="analytics-charts-grid">
          {pieData.length > 0 && (
            <div className="card analytics-chart-card">
              <h3 className="card-title">Répartition par statut</h3>
              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={4} dataKey="value">
                    {pieData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="analytics-legend">
                {pieData.map((d) => (
                  <div key={d.name} className="analytics-legend-item">
                    <span className="analytics-legend-dot" style={{ background: d.color }} />
                    <span>{d.name}: {d.value}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {barData.length > 0 && (
            <div className="card analytics-chart-card">
              <h3 className="card-title">Lignes par rapport</h3>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={barData}>
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="lignes" fill="#4F46E5" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {stats.recent_reports?.length > 0 && (
          <div className="card analytics-recent">
            <h3 className="card-title">5 derniers rapports</h3>
            <div className="analytics-recent-list">
              {stats.recent_reports.map((r) => (
                <Link key={r.id} to={`/dashboard/${r.dashboard_link}`} className="analytics-recent-item">
                  <span className="analytics-recent-title">{r.title}</span>
                  <span className={`badge badge-sm ${r.status === "completed" ? "badge-success" : r.status === "failed" ? "badge-error" : "badge-info"}`}>
                    {r.status}
                  </span>
                  <span className="analytics-recent-date">
                    {new Date(r.created_at).toLocaleDateString("fr-FR")}
                  </span>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
