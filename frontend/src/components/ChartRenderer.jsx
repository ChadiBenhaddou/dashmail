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
} from "recharts";

const COLORS = {
  primary: "#E8853D",
  positive: "#3DAA6D",
  negative: "#D94F4F",
  palette: ["#E8853D", "#2ABFBF", "#3DAA6D", "#D94F4F", "#1A1A2E", "#FF6B4A", "#B0B0BE"],
};

function formatValue(value) {
  if (typeof value !== "number") return value;
  if (Math.abs(value) >= 1000) return `${(value / 1000).toFixed(1)}k`;
  return value;
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div
      style={{
        background: "var(--c-sheet)",
        border: "1px solid var(--c-border)",
        borderRadius: "var(--r-xs)",
        padding: "8px 12px",
        fontSize: "12px",
        fontFamily: "var(--font-display)",
        boxShadow: "var(--shadow-sm)",
      }}
    >
      <p style={{ color: "var(--c-ink-muted)", margin: "0 0 4px" }}>{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color, margin: 0, fontWeight: 600 }}>
          {entry.name}: {typeof entry.value === "number" ? entry.value.toLocaleString() : entry.value}
        </p>
      ))}
    </div>
  );
}

function LineChartView({ data, xAxisKey, yAxisKey, colors }) {
  const stroke = colors?.[0] || COLORS.primary;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--c-border)" />
        <XAxis dataKey={xAxisKey} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <YAxis tickFormatter={formatValue} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <Tooltip content={<CustomTooltip />} />
        <Line
          type="monotone"
          dataKey={yAxisKey}
          stroke={stroke}
          strokeWidth={2}
          dot={{ r: 3, fill: stroke, strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

function BarChartView({ data, xAxisKey, yAxisKey, colors, horizontal }) {
  const fill = colors?.[0] || COLORS.primary;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} layout={horizontal ? "vertical" : "horizontal"}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--c-border)" />
        {horizontal ? (
          <>
            <XAxis type="number" tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
            <YAxis dataKey={xAxisKey} type="category" tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" width={80} />
          </>
        ) : (
          <>
            <XAxis dataKey={xAxisKey} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
            <YAxis tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
          </>
        )}
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey={yAxisKey} fill={fill} radius={[4, 4, 0, 0]}>
          {data.map((_, i) => (
            <Cell key={i} fill={colors?.[i % colors.length] || COLORS.palette[i % COLORS.palette.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

function PieChartView({ data, xAxisKey, yAxisKey, colors }) {
  const palette = colors?.length ? colors : COLORS.palette;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={90}
          innerRadius={50}
          dataKey={yAxisKey}
          nameKey={xAxisKey}
          paddingAngle={3}
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
  if (!ChartComponent)
    return (
      <p style={{ color: "var(--c-ink-muted)", fontSize: "13px" }}>
        Type non supporte: {type}
      </p>
    );

  return (
    <div>
      {title && <h3 className="card-title">{title}</h3>}
      <ChartComponent data={data} xAxisKey={xAxisKey} yAxisKey={yAxisKey} colors={colors} horizontal={horizontal} />
    </div>
  );
}

export default ChartRenderer;
