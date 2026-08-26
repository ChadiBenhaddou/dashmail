import Header from "./Header.jsx";

export default function Layout({ children }) {
  return (
    <div className="site-layout">
      <Header />
      <main className="site-main">{children}</main>
      <footer className="site-footer">
        <div className="site-footer-inner">
          <div className="site-footer-brand">
            <img src="/logo.svg" alt="Dashbail" className="site-footer-logo-img" />
            <span>Dashbail</span>
          </div>
          <div className="site-footer-links">
            <a href="/api/docs/" target="_blank" rel="noreferrer">API Docs</a>
            <a href="https://github.com/ChadiBenhaddou/dashmail" target="_blank" rel="noreferrer">GitHub</a>
            <a href="/">À propos</a>
          </div>
          <p className="site-footer-copy">© 2024 Dashbail — Analyse automatique de données</p>
        </div>
      </footer>
    </div>
  );
}
