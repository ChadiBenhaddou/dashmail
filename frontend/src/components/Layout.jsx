import Header from "./Header.jsx";

export default function Layout({ children }) {
  return (
    <div className="site-layout">
      <Header />
      <main className="site-main">{children}</main>
      <footer className="site-footer">
        <div className="site-footer-inner">
          <div className="site-footer-brand">
            <img src="/logo-icon.svg" alt="" className="site-footer-logo-img" />
            <span>dashbail</span>
          </div>
          <div className="site-footer-links">
            <a href="/api/docs/" target="_blank" rel="noreferrer">
              API
            </a>
            <a
              href="https://github.com/ChadiBenhaddou/dashmail"
              target="_blank"
              rel="noreferrer"
            >
              Github
            </a>
            <a href="/">Equipe</a>
          </div>
          <p className="site-footer-copy">
            dashbail · projet de fin d'etudes · 2024
          </p>
        </div>
      </footer>
    </div>
  );
}
