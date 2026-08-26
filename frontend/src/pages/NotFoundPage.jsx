import { Link } from "react-router-dom";

function NotFoundPage() {
  return (
    <div className="error-page">
      <h1>404</h1>
      <p>La page que vous recherchez n'existe pas.</p>
      <Link to="/" className="btn-primary">
        Retour à l'accueil
      </Link>
    </div>
  );
}

export default NotFoundPage;
