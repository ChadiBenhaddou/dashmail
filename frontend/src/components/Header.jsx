import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext.jsx";
import { useTheme } from "../contexts/ThemeContext.jsx";

export default function Header() {
  const { user, logout, isAuthenticated } = useAuth();
  const { dark, toggle } = useTheme();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const navLinks = [
    { to: "/upload", label: "Analyser" },
    ...(isAuthenticated ? [
      { to: "/reports", label: "Historique" },
      { to: "/analytics", label: "Analytics" },
    ] : []),
  ];

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="site-header-logo">
          <div className="site-header-logo-icon">D</div>
          <span className="site-header-logo-text">Dashboard X</span>
        </Link>

        <nav className={`site-nav ${menuOpen ? "site-nav-open" : ""}`}>
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`site-nav-link ${location.pathname === link.to ? "site-nav-link-active" : ""}`}
              onClick={() => setMenuOpen(false)}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="site-header-right">
          <button className="theme-toggle" onClick={toggle} aria-label="Changer de thème" title={dark ? "Mode clair" : "Mode sombre"}>
            {dark ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            )}
          </button>
          {isAuthenticated ? (
            <div className="site-user-menu">
              <button className="site-user-btn" onClick={() => setMenuOpen(!menuOpen)}>
                <div className="site-user-avatar">{user?.username?.[0]?.toUpperCase() || "U"}</div>
                <span className="site-user-name">{user?.username}</span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 9l6 6 6-6"/></svg>
              </button>
              {menuOpen && (
                <div className="site-user-dropdown">
                  <div className="site-user-dropdown-info">
                    <strong>{user?.username}</strong>
                    <span>{user?.email}</span>
                  </div>
                  <button className="site-user-dropdown-item" onClick={logout}>Déconnexion</button>
                </div>
              )}
            </div>
          ) : (
            <div className="site-auth-links">
              <Link to="/login" className="btn btn-secondary btn-sm">Connexion</Link>
              <Link to="/register" className="btn btn-primary btn-sm">S'inscrire</Link>
            </div>
          )}

          <button className="site-hamburger" onClick={() => setMenuOpen(!menuOpen)} aria-label="Menu">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              {menuOpen ? <path d="M18 6L6 18M6 6l12 12" /> : <path d="M3 12h18M3 6h18M3 18h18" />}
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}
