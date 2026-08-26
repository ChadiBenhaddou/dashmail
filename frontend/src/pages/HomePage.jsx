import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../contexts/AuthContext.jsx";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5, ease: "easeOut" } }),
};

const FEATURES = [
  { icon: "📊", title: "Analyse IA", desc: "OpenAI analyse automatiquement vos données et génère des insights pertinents." },
  { icon: "📈", title: "Graphiques auto", desc: "Des visualisations professionnelles créées automatiquement à partir de vos CSV/Excel." },
  { icon: "⚡", title: "Sans inscription", desc: "Envoyez votre fichier par email ou uploadez-le, le dashboard est prêt en secondes." },
  { icon: "📧", title: "Notification email", desc: "Recevez un lien vers votre dashboard par email dès que l'analyse est terminée." },
  { icon: "📄", title: "Export PDF", desc: "Téléchargez vos rapports et graphiques en PDF pour les partager." },
  { icon: "🔒", title: "Sécurisé", desc: "Vos données sont chiffrées et supprimées automatiquement après traitement." },
];

const STEPS = [
  { num: "1", title: "Envoyez votre fichier", desc: "Par email en pièce jointe ou via notre interface d'upload." },
  { num: "2", title: "L'IA analyse vos données", desc: "Nettoyage, détection de patterns, et génération d'insights automatiques." },
  { num: "3", title: "Recevez votre dashboard", desc: "Graphiques, KPIs, et analyses prêts à partager en un clic." },
];

const TECHS = [
  { name: "Django", color: "#092E20" },
  { name: "React", color: "#61DAFB" },
  { name: "PostgreSQL", color: "#4169E1" },
  { name: "Redis", color: "#DC382D" },
  { name: "Celery", color: "#A9CC54" },
  { name: "OpenAI", color: "#10A37F" },
  { name: "Docker", color: "#2496ED" },
  { name: "Recharts", color: "#FF6B6B" },
];

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="landing">
      {/* Hero */}
      <section className="landing-hero">
        <motion.div className="landing-hero-content" initial="hidden" animate="visible" variants={fadeUp}>
          <motion.div className="landing-hero-badge" variants={fadeUp} custom={0}>
            Propulsé par l'intelligence artificielle
          </motion.div>
          <motion.h1 className="landing-hero-title" variants={fadeUp} custom={1}>
            Transformez vos données en{" "}
            <span className="landing-hero-highlight">dashboards automatiques</span>
          </motion.h1>
          <motion.p className="landing-hero-subtitle" variants={fadeUp} custom={2}>
            Envoyez un fichier CSV ou Excel par email ou uploadez-le directement.
            Notre IA génère un dashboard professionnel avec graphiques, KPIs et insights en quelques secondes.
          </motion.p>
          <motion.div className="landing-hero-actions" variants={fadeUp} custom={3}>
            <Link to={isAuthenticated ? "/upload" : "/register"} className="btn btn-primary btn-lg">
              Commencer gratuitement
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </Link>
            <a href="#how-it-works" className="btn btn-secondary">En savoir plus</a>
          </motion.div>
        </motion.div>

        <motion.div
          className="landing-hero-visual"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <div className="landing-hero-mockup">
            <div className="mockup-header">
              <div className="mockup-dots"><span /><span /><span /></div>
              <div className="mockup-url">dashboard-x.app/dashboard/...</div>
            </div>
            <div className="mockup-body">
              <div className="mockup-kpi-row">
                <div className="mockup-kpi"><div className="mockup-kpi-val">1,250</div><div className="mockup-kpi-label">Lignes analysées</div></div>
                <div className="mockup-kpi"><div className="mockup-kpi-val">92%</div><div className="mockup-kpi-label">Qualité données</div></div>
                <div className="mockup-kpi mockup-kpi-accent"><div className="mockup-kpi-val">+15%</div><div className="mockup-kpi-label">Croissance</div></div>
              </div>
              <div className="mockup-chart">
                <svg viewBox="0 0 300 100" className="mockup-chart-svg">
                  <polyline points="0,80 50,60 100,65 150,40 200,30 250,45 300,20" fill="none" stroke="#4F46E5" strokeWidth="3" />
                  <polyline points="0,90 50,80 100,75 150,70 200,60 250,55 300,50" fill="none" stroke="#10B981" strokeWidth="2" strokeDasharray="5,5" />
                </svg>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="landing-section">
        <motion.div className="landing-section-header" initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
          <h2 className="landing-section-title">Comment ça marche</h2>
          <p className="landing-section-subtitle">Trois étapes simples pour obtenir votre dashboard</p>
        </motion.div>
        <div className="landing-steps">
          {STEPS.map((step, i) => (
            <motion.div key={i} className="landing-step" initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={i}>
              <div className="landing-step-num">{step.num}</div>
              <h3 className="landing-step-title">{step.title}</h3>
              <p className="landing-step-desc">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="landing-section landing-section-alt">
        <motion.div className="landing-section-header" initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
          <h2 className="landing-section-title">Fonctionnalités</h2>
          <p className="landing-section-subtitle">Tout ce dont vous avez besoin pour analyser vos données</p>
        </motion.div>
        <div className="landing-features">
          {FEATURES.map((f, i) => (
            <motion.div key={i} className="landing-feature" initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={i}>
              <div className="landing-feature-icon">{f.icon}</div>
              <h3 className="landing-feature-title">{f.title}</h3>
              <p className="landing-feature-desc">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Tech stack */}
      <section className="landing-section">
        <motion.div className="landing-section-header" initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
          <h2 className="landing-section-title">Stack technique</h2>
          <p className="landing-section-subtitle">Technologies modernes pour une plateforme performante</p>
        </motion.div>
        <div className="landing-techs">
          {TECHS.map((t, i) => (
            <motion.div key={i} className="landing-tech" initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={i}>
              <div className="landing-tech-dot" style={{ background: t.color }} />
              <span>{t.name}</span>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="landing-cta">
        <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
          <h2 className="landing-cta-title">Prêt à analyser vos données ?</h2>
          <p className="landing-cta-subtitle">Créez votre compte gratuit et uploadez votre premier fichier.</p>
          <Link to={isAuthenticated ? "/upload" : "/register"} className="btn btn-primary btn-lg">
            Commencer maintenant
          </Link>
        </motion.div>
      </section>
    </div>
  );
}
