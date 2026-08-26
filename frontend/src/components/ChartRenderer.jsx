import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Label,
} from "recharts";

const COLORS = {
  primary: "#4F46E5",
  positive: "#10B981",
  negative: "#EF4444",
  neutral: ["#6B7280", "#9CA3AF", "#D1D5DB", "#E5E7EB", "#374151", "#4B5563"],
};

function formatValue(value) {
  if (typeof value !== "number") return value;
  if (Math.abs(value) >= 1000) {
    return `${(value / 1000).toFixed(1)}k`;
  }
  return value;
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="chart-tooltip">
      <p className="tooltip-label">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }}>
          {entry.name}: {typeof entry.value === "number" ? entry.value.toLocaleString() : entry.value}
        </p>
      ))}
    </div>
  );
}

function LineChartView({ data, xAxisKey, yAxisKey, colors }) {
  const stroke = colors?.[0] || COLORS.primary;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        <XAxis dataKey={xAxisKey} tick={{ fontSize: 12 }} stroke="#9CA3AF" />
        <YAxis tickFormatter={formatValue} tick={{ fontSize: 12 }} stroke="#9CA3AF" />
        <Tooltip content={<CustomTooltip />} />
        <Line
          type="monotone"
          dataKey={yAxisKey}
          stroke={stroke}
          strokeWidth={2}
          dot={{ r: 4, fill: stroke }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

function BarChartView({ data, xAxisKey, yAxisKey, colors, horizontal }) {
  const fill = colors?.[0] || COLORS.primary;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout={horizontal ? "vertical" : "horizontal"}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
        {horizontal ? (
          <>
            <XAxis type="number" tick={{ fontSize: 12 }} stroke="#9CA3AF" />
            <YAxis dataKey={xAxisKey} type="category" tick={{ fontSize: 12 }} stroke="#9CA3AF" width={80} />
          </>
        ) : (
          <>
            <XAxis dataKey={xAxisKey} tick={{ fontSize: 12 }} stroke="#9CA3AF" />
            <YAxis tick={{ fontSize: 12 }} stroke="#9CA3AF" />
          </>
        )}
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey={yAxisKey} fill={fill} radius={[4, 4, 0, 0]} label={{ position: "top", fontSize: 11, fill: "#6B7280" }}>
          {data.map((_, i) => (
            <Cell key={i} fill={colors?.[i % colors.length] || fill} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

function PieChartView({ data, xAxisKey, yAxisKey, colors }) {
  const palette = colors?.length ? colors : [COLORS.primary, COLORS.positive, COLORS.negative, ...COLORS.neutral];
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={100}
          dataKey={yAxisKey}
          nameKey={xAxisKey}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((_, i) => (
            <Cell key={i} fill={palette[i % palette.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

const CHART_MAP = {
  line: LineChartView,
  bar: BarChartView,
  pie: PieChartView,
};

function ChartRenderer({ type, data, title, xAxisKey, yAxisKey, colors, horizontal }) {
  const ChartComponent = CHART_MAP[type];
  if (!ChartComponent) return <p>Type de graphique non supporté: {type}</p>;

  return (
    <div className="chart-wrapper">
      {title && <h3 className="chart-title">{title}</h3>}
      <ChartComponent data={data} xAxisKey={xAxisKey} yAxisKey={yAxisKey} colors={colors} horizontal={horizontal} />
    </div>
  );
}

export default ChartRenderer;
