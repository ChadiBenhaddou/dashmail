import { useState, useEffect } from "react";

const STEPS = ["Lecture du fichier", "Analyse des données", "Génération du rapport"];

function LoadingState() {
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
    <div className="loading-state" role="status" aria-live="polite" aria-label="Chargement du rapport">
      <div className="spinner" aria-hidden="true" />
      <h2>Chargement du rapport…</h2>
      <p className="loading-sub">Nous préparons vos graphiques et vos analyses.</p>
      <div className="progress-bar-wrap" role="progressbar" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100} aria-label={`Progression: ${progress}%`}>
        <div className="progress-bar" style={{ width: `${progress}%` }} />
      </div>
      <div className="steps-pipeline" aria-label="Étapes de chargement">
        {STEPS.map((step, i) => (
          <span key={i} className={`step ${i <= activeStep ? "step-active" : ""}`}>
            {step}
            {i < STEPS.length - 1 && <span className="step-arrow" aria-hidden="true"> → </span>}
          </span>
        ))}
      </div>
    </div>
  );
}

export default LoadingState;
