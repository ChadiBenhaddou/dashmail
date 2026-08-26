import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getStats } from "../services/api.js";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = {
  completed: "#3DAA6D",
  processing: "#E8853D",
  failed: "#D94F4F",
  pending: "#B0B0BE",
};

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStats()
      .then(setStats)
      .catch(() =>
        setStats({
          total: 0,
          completed: 0,
          failed: 0,
          processing: 0,
          total_size_bytes: 0,
          recent_reports: [],
        })
      )
      .finally(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="upload-page">
        <div className="loading-spinner" />
      </div>
    );
  if (!stats) return null;

  const pieData = [
    { name: "Termines", value: stats.completed, color: COLORS.completed },
    { name: "En cours", value: stats.processing, color: COLORS.processing },
    { name: "Echoues", value: stats.failed, color: COLORS.failed },
  ].filter((d) => d.value > 0);

  const barData = stats.recent_reports.map((r) => ({
    name: r.title?.substring(0, 14) || "Sans titre",
    lignes: r.row_count || 0,
  }));

  return (
    <div className="analytics-page">
      <div className="analytics-container">
        <div className="reports-header">
          <div>
            <h1 className="reports-title">Statistiques</h1>
            <p className="reports-subtitle">Vue d'ensemble</p>
          </div>
        </div>

        <div className="analytics-kpi-grid">
          <div className="analytics-kpi">
            <span className="analytics-kpi-value">{stats.total}</span>
            <span className="analytics-kpi-label">Rapports</span>
          </div>
          <div className="analytics-kpi analytics-kpi-success">
            <span className="analytics-kpi-value">{stats.completed}</span>
            <span className="analytics-kpi-label">Termines</span>
          </div>
          <div className="analytics-kpi analytics-kpi-error">
            <span className="analytics-kpi-value">{stats.failed}</span>
            <span className="analytics-kpi-label">Echoues</span>
          </div>
          <div className="analytics-kpi analytics-kpi-primary">
            <span className="analytics-kpi-value">
              {(stats.total_size_bytes / (1024 * 1024)).toFixed(1)} Mo
            </span>
            <span className="analytics-kpi-label">Donnees traitees</span>
          </div>
        </div>

        <div className="analytics-charts-grid">
          {pieData.length > 0 && (
            <div className="card analytics-chart-card">
              <h3 className="card-title">Repartition</h3>
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {pieData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="analytics-legend">
                {pieData.map((d) => (
                  <div key={d.name} className="analytics-legend-item">
                    <span
                      className="analytics-legend-dot"
                      style={{ background: d.color }}
                    />
                    <span>
                      {d.name}: {d.value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {barData.length > 0 && (
            <div className="card analytics-chart-card">
              <h3 className="card-title">Lignes par rapport</h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={barData}>
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar
                    dataKey="lignes"
                    fill="#E8853D"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {stats.recent_reports?.length > 0 && (
          <div className="card analytics-recent">
            <h3 className="card-title">Derniers rapports</h3>
            <div className="analytics-recent-list">
              {stats.recent_reports.map((r) => (
                <Link
                  key={r.id}
                  to={`/dashboard/${r.dashboard_link}`}
                  className="analytics-recent-item"
                >
                  <span className="analytics-recent-title">{r.title}</span>
                  <span
                    className={`badge badge-sm ${
                      r.status === "completed"
                        ? "badge-success"
                        : r.status === "failed"
                        ? "badge-error"
                        : "badge-info"
                    }`}
                  >
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
