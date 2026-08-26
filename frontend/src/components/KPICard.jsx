import { useEffect, useState } from "react";

function AnimatedNumber({ value, duration = 1200 }) {
  const [display, setDisplay] = useState(0);
  const numValue = Number(value) || 0;

  useEffect(() => {
    const start = performance.now();
    const from = 0;
    const animate = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(from + (numValue - from) * eased);
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [numValue, duration]);

  const formatted = numValue >= 1000
    ? Math.round(display).toLocaleString("fr-FR")
    : Number.isInteger(numValue)
      ? Math.round(display).toString()
      : display.toFixed(1);

  return <span>{formatted}</span>;
}

function KPICard({ label, value, variation }) {
  const hasVariation = variation != null && !Number.isNaN(Number(variation));
  const numericVariation = hasVariation ? Number(variation) : 0;
  const isPositive = numericVariation >= 0;

  return (
    <div className="card kpi-card" role="figure" aria-label={label}>
      <p className="kpi-label">{label}</p>
      <p className="kpi-value">
        <AnimatedNumber value={value} />
      </p>
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
