import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login } from "../services/api.js";
import { useAuth } from "../contexts/AuthContext.jsx";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await login(email, password);
      setUser(res.user);
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">
          <img src="/logo-icon.svg" alt="" className="auth-logo-img" />
        </div>
        <h1 className="auth-title">Bon retour</h1>
        <p className="auth-subtitle">Connectez-vous pour acceder a vos rapports</p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="vous@example.com"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Mot de passe</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="********"
              required
            />
          </div>
          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? (
              <span className="btn-loading">
                <span className="spinner-small" />
                Connexion...
              </span>
            ) : (
              "Se connecter"
            )}
          </button>
        </form>

        <p className="auth-footer">
          Pas encore de compte ?{" "}
          <Link to="/register" className="auth-link">
            Creer un compte
          </Link>
        </p>
      </div>
    </div>
  );
}
