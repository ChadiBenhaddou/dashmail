import { useState, useEffect } from "react";

const STEPS = ["Lecture du fichier", "Analyse des donnees", "Generation du rapport"];

function LoadingState({ status }) {
  const [progress, setProgress] = useState(0);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((p) => {
        const next = Math.min(p + 1, 100);
        if (next < 33) setActiveStep(0);
        else if (next < 66) setActiveStep(1);
        else setActiveStep(2);
        return next;
      });
    }, 100);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-page" role="status" aria-live="polite">
      <div className="loading-spinner" aria-hidden="true" />
      <h2
        style={{
          fontFamily: "var(--font-display)",
          fontSize: "18px",
          fontWeight: 600,
          color: "var(--c-ink)",
        }}
      >
        {status === "processing" ? "Analyse en cours..." : "Chargement..."}
      </h2>
      <p
        style={{
          fontSize: "14px",
          color: "var(--c-ink-muted)",
          marginTop: "-16px",
        }}
      >
        {status === "processing"
          ? "L'IA est en train d'analyser vos donnees."
          : "On prepare vos graphiques et analyses."}
      </p>
      <div
        className="loading-progress"
        role="progressbar"
        aria-valuenow={progress}
      >
        <div
          className="loading-progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="loading-steps">
        {STEPS.map((step, i) => (
          <span key={i} className={`loading-step ${i <= activeStep ? "active" : ""}`}>
            <span className="loading-step-dot" />
            {step}
          </span>
        ))}
      </div>
    </div>
  );
}

export default LoadingState;
