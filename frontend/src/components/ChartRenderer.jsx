import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
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

let stackCounter = 0;

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
        <p key={i} style={{ color: entry.color || entry.stroke || entry.fill, margin: 0, fontWeight: 600 }}>
          {entry.name}: {typeof entry.value === "number" ? entry.value.toLocaleString() : entry.value}
        </p>
      ))}
    </div>
  );
}

function pickColors(colors, fallback) {
  return colors?.length ? colors : fallback;
}

function MultiSeries({ render, chart, fallbackColors }) {
  const { seriesKeys = [], colors, xAxisKey, yAxisKey } = chart;
  const palette = pickColors(colors, fallbackColors);
  return (
    <>
      {seriesKeys.map((key, i) =>
        render(key, palette[i % palette.length], i)
      )}
      <Legend />
    </>
  );
}

function LineChartView({ data, xAxisKey, yAxisKey, colors, chart }) {
  const stroke = colors?.[0] || COLORS.primary;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--c-border)" />
        <XAxis dataKey={xAxisKey} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <YAxis tickFormatter={formatValue} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <Tooltip content={<CustomTooltip />} />
        {chart?.seriesKeys?.length ? (
          <MultiSeries
            chart={chart}
            fallbackColors={COLORS.palette}
            render={(key, color) => (
              <Line key={key} type="monotone" dataKey={key} stroke={color}
                strokeWidth={2} dot={{ r: 3, fill: color, strokeWidth: 0 }} activeDot={{ r: 5 }} />
            )}
          />
        ) : (
          <Line type="monotone" dataKey={yAxisKey} stroke={stroke} strokeWidth={2}
            dot={{ r: 3, fill: stroke, strokeWidth: 0 }} activeDot={{ r: 5 }} />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
}

function AreaChartView({ data, xAxisKey, yAxisKey, colors, chart }) {
  const stroke = colors?.[0] || COLORS.primary;
  const gradId = `grad-${(stackCounter += 1)}`;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={stroke} stopOpacity={0.5} />
            <stop offset="95%" stopColor={stroke} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--c-border)" />
        <XAxis dataKey={xAxisKey} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <YAxis tickFormatter={formatValue} tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <Tooltip content={<CustomTooltip />} />
        {chart?.seriesKeys?.length ? (
          <MultiSeries
            chart={chart}
            fallbackColors={COLORS.palette}
            render={(key, color) => (
              <Area key={key} type="monotone" dataKey={key} stroke={color}
                fill={color} fillOpacity={0.15} />
            )}
          />
        ) : (
          <Area type="monotone" dataKey={yAxisKey} stroke={stroke}
            fill={`url(#${gradId})`} strokeWidth={2} />
        )}
      </AreaChart>
    </ResponsiveContainer>
  );
}

function BarChartView({ data, xAxisKey, yAxisKey, colors, horizontal, chart }) {
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
        {chart?.seriesKeys?.length ? (
          <MultiSeries
            chart={chart}
            fallbackColors={COLORS.palette}
            render={(key, color) => (
              <Bar key={key} dataKey={key} fill={color} radius={[4, 4, 0, 0]} />
            )}
          />
        ) : (
          <Bar dataKey={yAxisKey} fill={fill} radius={[4, 4, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={colors?.[i % colors.length] || COLORS.palette[i % COLORS.palette.length]} />
            ))}
          </Bar>
        )}
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

function ScatterChartView({ data, xAxisKey, yAxisKey, colors }) {
  const fill = colors?.[0] || COLORS.primary;
  const scatterData = (data || []).map((d) => ({
    x: d[xAxisKey],
    y: d[yAxisKey],
  }));
  return (
    <ResponsiveContainer width="100%" height={280}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--c-border)" />
        <XAxis type="number" dataKey="x" name={xAxisKey} tickFormatter={formatValue}
          tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <YAxis type="number" dataKey="y" name={yAxisKey} tickFormatter={formatValue}
          tick={{ fontSize: 11, fill: "var(--c-ink-muted)" }} stroke="var(--c-border)" />
        <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: "3 3" }} />
        <Scatter data={scatterData} fill={fill} fillOpacity={0.6} />
      </ScatterChart>
    </ResponsiveContainer>
  );
}

function RadarChartView({ data, xAxisKey, yAxisKey, colors }) {
  const stroke = colors?.[0] || COLORS.primary;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
        <PolarGrid stroke="var(--c-border)" />
        <PolarAngleAxis dataKey={xAxisKey} tick={{ fontSize: 10, fill: "var(--c-ink-muted)" }} />
        <PolarRadiusAxis tickFormatter={formatValue} tick={{ fontSize: 9, fill: "var(--c-ink-faint)" }} />
        <Radar name={yAxisKey} dataKey={yAxisKey} stroke={stroke} fill={stroke} fillOpacity={0.3} />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
      </RadarChart>
    </ResponsiveContainer>
  );
}

const CHART_MAP = {
  line: LineChartView,
  bar: BarChartView,
  pie: PieChartView,
  area: AreaChartView,
  scatter: ScatterChartView,
  radar: RadarChartView,
};

function ChartRenderer({ type, data, title, xAxisKey, yAxisKey, colors, horizontal, chart }) {
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
      <ChartComponent data={data} xAxisKey={xAxisKey} yAxisKey={yAxisKey} colors={colors} horizontal={horizontal} chart={{ ...chart, xAxisKey, yAxisKey }} />
      {chart?.description && (
        <p className="chart-description">{chart.description}</p>
      )}
    </div>
  );
}

export default ChartRenderer;
