import { Link } from "react-router-dom";

function ErrorState({ error, onRetry }) {
  return (
    <div className="error-page" role="alert">
      <div className="error-icon" aria-hidden="true">
        !
      </div>
      <h2
        style={{
          fontFamily: "var(--font-display)",
          fontSize: "20px",
          fontWeight: 700,
          color: "var(--c-ink)",
          margin: "0 0 6px",
        }}
      >
        Oups.
      </h2>
      <p className="error-message">
        {error?.message || "Le lien a peut-etre expire ou est invalide."}
      </p>
      <div className="error-actions">
        {onRetry && (
          <button className="btn btn-primary" onClick={onRetry}>
            Reessayer
          </button>
        )}
        <Link to="/" className="btn btn-secondary">
          Retour
        </Link>
      </div>
    </div>
  );
}

export default ErrorState;
