import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../contexts/AuthContext.jsx";

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.45, ease: [0.25, 0.46, 0.45, 0.94] },
  }),
};

const FEATURES = [
  {
    icon: "01",
    title: "Envoyez vos donnees",
    desc: "Un CSV, un Excel — glissez-deposez ou envoyez par email. On s'occupe du reste.",
  },
  {
    icon: "02",
    title: "L'IA fait le gros oeuvre",
    desc: "Nettoyage, detection de patterns, insights pertinents. Tout est automatise.",
  },
  {
    icon: "03",
    title: "Dashboard pret",
    desc: "Graphiques, KPIs, qualite des donnees. Partageable en un clic.",
  },
];

const TOOLS = [
  { name: "Django", dot: "#0C4B33" },
  { name: "React", dot: "#61DAFB" },
  { name: "PostgreSQL", dot: "#336791" },
  { name: "Redis", dot: "#DC382D" },
  { name: "Celery", dot: "#A9CC54" },
  { name: "OpenAI", dot: "#10A37F" },
  { name: "Docker", dot: "#2496ED" },
];

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="landing">
      {/* Hero — asymmetric */}
      <section className="landing-hero">
        <motion.div
          className="landing-hero-content"
          initial="hidden"
          animate="visible"
          variants={fadeUp}
        >
          <motion.div className="landing-hero-badge" variants={fadeUp} custom={0}>
            propulse par l'ia
          </motion.div>

          <motion.h1 className="landing-hero-title" variants={fadeUp} custom={1}>
            Vos donnees merite{"\n"}
            <span className="landing-hero-highlight">meilleur qu'un tableur</span>
          </motion.h1>

          <motion.p
            className="landing-hero-subtitle"
            variants={fadeUp}
            custom={2}
          >
            Uploadez un fichier ou envoyez-le par email. Dashbail analyse,
            nettoie et transforme vos donnees en un dashboard complet avec
            graphiques, KPIs et insights — en quelques secondes.
          </motion.p>

          <motion.div className="landing-hero-actions" variants={fadeUp} custom={3}>
            <Link
              to={isAuthenticated ? "/upload" : "/register"}
              className="btn btn-accent btn-lg"
            >
              Essayer maintenant
              <svg
                width="15"
                height="15"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </Link>
            <a href="#how" className="btn btn-secondary">
              Comment ca marche
            </a>
          </motion.div>
        </motion.div>

        <motion.div
          className="landing-hero-visual"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35, duration: 0.55, ease: [0.25, 0.46, 0.45, 0.94] }}
        >
          <div className="landing-hero-mockup">
            <div className="mockup-header">
              <div className="mockup-dots">
                <span />
                <span />
                <span />
              </div>
              <div className="mockup-url">dashbail.app/dashboard/...</div>
            </div>
            <div className="mockup-body">
              <div className="mockup-kpi-row">
                <div className="mockup-kpi">
                  <div className="mockup-kpi-val">1,247</div>
                  <div className="mockup-kpi-label">Lignes</div>
                </div>
                <div className="mockup-kpi">
                  <div className="mockup-kpi-val">94%</div>
                  <div className="mockup-kpi-label">Qualite</div>
                </div>
                <div className="mockup-kpi mockup-kpi-accent">
                  <div className="mockup-kpi-val">+18%</div>
                  <div className="mockup-kpi-label">Evolution</div>
                </div>
              </div>
              <div className="mockup-chart">
                <svg viewBox="0 0 300 90" className="mockup-chart-svg">
                  <defs>
                    <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#E8853D" stopOpacity="0.2" />
                      <stop offset="100%" stopColor="#E8853D" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M0,75 Q30,68 60,60 T120,42 T180,35 T240,28 T300,15"
                    fill="none"
                    stroke="#E8853D"
                    strokeWidth="2.5"
                  />
                  <path
                    d="M0,75 Q30,68 60,60 T120,42 T180,35 T240,28 T300,15 L300,90 L0,90Z"
                    fill="url(#chartGrad)"
                  />
                  <path
                    d="M0,82 Q40,78 80,72 T160,64 T240,58 T300,52"
                    fill="none"
                    stroke="#3DAA6D"
                    strokeWidth="1.5"
                    strokeDasharray="4,4"
                    opacity="0.5"
                  />
                </svg>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* How it works */}
      <section id="how" className="landing-section">
        <motion.div
          className="landing-section-header"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={fadeUp}
        >
          <h2 className="landing-section-title">Trois etapes, c'est tout</h2>
          <p className="landing-section-subtitle">
            Pas de configuration. Pas de tuto. Juste vos donnees.
          </p>
        </motion.div>

        <div className="landing-steps">
          {FEATURES.map((f, i) => (
            <motion.div
              key={i}
              className="landing-step"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-40px" }}
              variants={fadeUp}
              custom={i}
            >
              <div className="landing-step-num">{f.icon}</div>
              <h3 className="landing-step-title">{f.title}</h3>
              <p className="landing-step-desc">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Features — 2 col asymmetric */}
      <section className="landing-section landing-section-alt">
        <motion.div
          className="landing-section-header"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={fadeUp}
        >
          <h2 className="landing-section-title">Ce qu'on fait pour vous</h2>
          <p className="landing-section-subtitle">
            Derriere la simplicite, une pipeline de donnees serieuse
          </p>
        </motion.div>

        <div className="landing-features">
          {[
            {
              title: "Analyse IA",
              desc: "OpenAI lit vos colonnes, comprend le contexte et sort des insights que vous n'auriez pas trouves seul.",
            },
            {
              title: "Graphiques auto",
              desc: "Barres, courbes, pie-charts — choisis selon le type de donnees. Pas besoin de design.",
            },
            {
              title: "Email vers dashboard",
              desc: "Envoyez en PJ, recevez un lien. Aucune inscription pour commencer.",
            },
            {
              title: "Export PDF",
              desc: "Un clic pour telecharger un rapport propre. Pret pour la reunion de 9h.",
            },
            {
              title: "Partage securise",
              desc: "Lien temporaire, pas de mot de passe. Vos donnees restent privees.",
            },
            {
              title: "Cache intelligent",
              desc: "Pas de re-traitement inutile. Les donnees deja analysees sont en memoire.",
            },
          ].map((f, i) => (
            <motion.div
              key={i}
              className="landing-feature"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-40px" }}
              variants={fadeUp}
              custom={i}
            >
              <h3 className="landing-feature-title">{f.title}</h3>
              <p className="landing-feature-desc">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Tech */}
      <section className="landing-section">
        <motion.div
          className="landing-section-header"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={fadeUp}
        >
          <h2 className="landing-section-title">Sous le capot</h2>
        </motion.div>
        <div className="landing-techs">
          {TOOLS.map((t, i) => (
            <motion.div
              key={i}
              className="landing-tech"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              custom={i}
            >
              <div className="landing-tech-dot" style={{ background: t.dot }} />
              <span>{t.name}</span>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="landing-cta">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={fadeUp}
        >
          <h2 className="landing-cta-title">
            Pas de temps a perdre avec des tableurs ?
          </h2>
          <p className="landing-cta-subtitle">
            Un fichier, quelques secondes, un dashboard. C'est tout.
          </p>
          <Link
            to={isAuthenticated ? "/upload" : "/register"}
            className="btn btn-accent btn-lg"
          >
            Commencer
          </Link>
        </motion.div>
      </section>
    </div>
  );
}
