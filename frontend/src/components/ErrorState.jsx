import { Link } from "react-router-dom";

function ErrorState({ error, onRetry }) {
  return (
    <div className="error-state" role="alert" aria-label="Erreur de chargement">
      <div className="error-icon" aria-hidden="true">!</div>
      <h2>Impossible de charger ce rapport</h2>
      <p className="error-sub">
        {error?.message || "Le lien a peut-être expiré ou le lien est invalide."}
      </p>
      <div className="error-actions">
        {onRetry && (
          <button className="btn-primary" onClick={onRetry} aria-label="Réessayer le chargement">
            Réessayer
          </button>
        )}
        <Link to="/" className="btn-secondary" aria-label="Retour à l'accueil">
          Fermer
        </Link>
      </div>
    </div>
  );
}

export default ErrorState;
