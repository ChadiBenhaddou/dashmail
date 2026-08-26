# Prompt PFE — Construction complète de la plateforme Dashbail

**Objectif :** Transformer le code existant (backend Django fonctionnel + frontend basique) en une plateforme SaaS complète et visuellement impressionnante, prête pour la soutenance PFE.

---

## Contexte du projet existant

Monorepo `backend/` + `frontend/` + `docker-compose.yml`.

**Backend (85%) :** Django 5 + DRF + Celery/Redis + PostgreSQL + OpenAI. Pipeline complet : parsing → cleaning → LLM → Recharts JSON → email. Endpoint public `GET /api/dashboard/<uuid>/`. 12 tests OK.

**Frontend (30%) :** React 18 + Vite + Recharts. Dashboard view fonctionnante. MANQUANT : Landing page, upload UI, auth, historique, navigation, status temps réel, PDF, Swagger, dark mode.

---

## Stack finale

| Couche | Tech |
|--------|------|
| Backend | Django 5 + DRF |
| Auth | djangorestframework-simplejwt |
| Async | Celery 5 + Redis |
| DB | PostgreSQL 16 |
| Frontend | React 18 + Vite 5 |
| Charts | Recharts 2.x |
| Animations | framer-motion 12.x |
| Style | CSS custom properties |
| API Docs | drf-spectacular |
| PDF | xhtml2pdf |
| LLM | OpenAI API |
| Infra | Docker Compose |

---

## Phases

### Phase 0 — Corrections critiques
0.1 [Ayoub] Fixer seed data (clés charts, format insights, scale quality)
0.2 [Ayoub] Ajouter download_url à l'API
0.3 [Ayoub] Corriger titre HTML → "Dashbail"

### Phase 1 — Auth JWT
1.1 [Ayoub] Backend JWT (register, login, refresh, me)
1.2 [Haitem] Pages Auth React + AuthContext + ProtectedRoute
1.3 [Haitem] Intégrer auth dans le Dashboard

### Phase 2 — Upload + Pipeline
2.1 [Ayoub] Endpoint POST /api/reports/upload/
2.2 [Haitem] Page Upload drag-and-drop
2.3 [Ayoub, Haitem] Status polling (2s interval)

### Phase 3 — Historique + Analytics
3.1 [Ayoub] Endpoint listing + stats
3.2 [Haitem] Page Historique (tableau/filtres)
3.3 [Haitem] Page Analytics (graphiques d'usage)

### Phase 4 — Navigation + Layout
4.1 [Haitem] Header/Navbar sticky
4.2 [Haitem] Layout partagé (Header + Footer)
4.3 [Haitem] Responsive global

### Phase 5 — Landing Page
5.1 [Haitem] HomePage complète (Hero + Comment ça marche + Features + Tech)
5.2 [Haitem] Animations framer-motion

### Phase 6 — Dark Mode + Extras
6.1 [Haitem] Dark Mode (ThemeContext + CSS variables)
6.2 [Haitem] Partage de rapport (copy link + share)
6.3 [Ayoub, Haitem] Graphiques animés (compteurs KPI)

### Phase 7 — Backend extras
7.1 [Ayoub] Swagger/OpenAPI (drf-spectacular)
7.2 [Ayoub, Moussa] PDF Export (xhtml2pdf)
7.3 [Ayoub] Rate limiting
7.4 [Ayoub, Moussa] LLM Fallback heuristique

### Phase 8 — Tests
8.1 [Tous] Tests backend manquants (25+ objectif)
8.2 [Tous] Tests E2E complets
8.3 [Tous] Linting ruff

### Phase 9 — Déploiement + Doc
9.1 [Chadi] Déploiement Scaleway/Railway
9.2 [Tous] README final avec screenshots
9.3 [Tous] Guide de démo (DEMO.md)
9.4 [Tous] Présentation finale

---

## Critères de validation
1. docker-compose up → 5 services OK
2. seed_data → 5 rapports valides
3. Dashboard API → données complètes
4. Upload UI → dashboard généré
5. Auth → register + login + tokens
6. Tests → 25+ OK
7. Frontend → toutes pages navigables + responsive
8. Dark mode → toggle fonctionne
9. Swagger → /api/docs/ fonctionne
10. PDF → téléchargement valide
11. Landing → visuellement pro
12. Animations → fluides
