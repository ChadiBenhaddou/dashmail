function KPICard({ label, value, variation }) {
  const hasVariation = variation != null && !Number.isNaN(Number(variation));
  const numericVariation = hasVariation ? Number(variation) : 0;
  const isPositive = numericVariation >= 0;

  return (
    <div className="card kpi-card" role="figure" aria-label={label}>
      <p className="kpi-label">{label}</p>
      <p className="kpi-value">{value}</p>
      {hasVariation && (
        <p className={`kpi-variation ${isPositive ? "positive" : "negative"}`}>
          <span className="kpi-arrow" aria-hidden="true">{isPositive ? "↑" : "↓"}</span>
          {Math.abs(numericVariation)}%
        </p>
      )}
    </div>
  );
}

export default KPICard;
