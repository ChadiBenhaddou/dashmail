# Dashbail

Plateforme SaaS de **génération automatique de rapports visuels** à partir de
fichiers **CSV / Excel** envoyés par **email** ou **upload direct**.

Propulsée par l'**intelligence artificielle** (OpenAI GPT-4o) pour analyser
vos données et créer des dashboards professionnels avec graphiques, KPIs et insights.

## Stack technique

| Couche | Technologie |
|--------|------------|
| Backend | Django 5 + Django REST Framework + Celery + Redis + PostgreSQL |
| Auth | JWT (djangorestframework-simplejwt) |
| Frontend | React 18 (Vite) + Recharts + framer-motion |
| LLM | OpenAI GPT-4o (avec fallback heuristique) |
| PDF | xhtml2pdf |
| API Docs | drf-spectacular (Swagger/OpenAPI) |
| Conteneurisation | Docker + docker-compose |

## Fonctionnalités

### Utilisateur
- **Upload drag-and-drop** — Uploadez vos CSV/XLSX directement depuis l'interface
- **Ingestion par email** — Envoyez vos fichiers en pièce jointe, le dashboard est créé automatiquement
- **Dashboard interactif** — Graphiques Recharts (bar, line, pie), KPIs animés, insights IA
- **Statut temps réel** — Polling automatique pendant le traitement (parsing → analyse → génération)
- **Export PDF** — Téléchargez vos rapports en PDF
- **Partage** — Copiez le lien de votre dashboard pour le partager
- **Historique** — Liste de tous vos rapports avec filtres et recherche
- **Analytics** — Vue d'ensemble de votre utilisation (stats, graphiques)

### Technique
- **Auth JWT** — Register, login, tokens avec auto-refresh
- **Dark mode** — Toggle clair/sombre avec persistance
- **Animations** — framer-motion sur la landing, compteurs KPI animés
- **Swagger** — Documentation interactive de l'API sur `/api/docs/`
- **Rate limiting** — 100 requêtes/heure (anon), 1000/heure (auth)
- **Cache Redis** — Dashboard mis en cache 1h
- **LLM Fallback** — Si OpenAI échoue, analyse heuristique automatique
- **32 tests** — Auth, parsing, cleaning, charts, PDF, vues

## Installation locale

### Prérequis

- [Docker](https://www.docker.com/) et Docker Compose
- Clé API OpenAI (optionnelle, fallback heuristique disponible)

### Étapes

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/ChadiBenhaddou/dashmail.git
   cd dashmail
   ```

2. Copier `.env.example` en `.env` et renseigner les variables :

   ```bash
   cp .env.example .env
   ```

3. Lancer la stack :

   ```bash
   docker-compose up --build
   ```

4. Créer un superuser (optionnel) :

   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. Charger les données de test :

   ```bash
   docker-compose exec backend python manage.py seed_data
   ```

### Accès aux services

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/api/docs/ |
| Admin Django | http://localhost:8000/admin/ |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## API Endpoints

| Endpoint | Méthode | Auth | Description |
|----------|---------|------|-------------|
| `/api/auth/register/` | POST | Non | Créer un compte |
| `/api/auth/login/` | POST | Non | Connexion (retourne JWT) |
| `/api/auth/me/` | GET | Oui | Profil utilisateur |
| `/api/reports/` | GET | Oui | Liste des rapports |
| `/api/reports/upload/` | POST | Oui | Uploader un fichier |
| `/api/dashboard/<uuid>/` | GET | Non | Données du dashboard |
| `/api/dashboard/<uuid>/pdf/` | GET | Non | Télécharger le PDF |
| `/api/stats/` | GET | Oui | Statistiques d'utilisation |
| `/api/docs/` | GET | Non | Swagger UI |
| `/admin/` | GET | Admin | Interface d'administration |

## Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DJANGO_SECRET_KEY` | Clé secrète Django | `change-me-in-production` |
| `DJANGO_DEBUG` | Mode debug | `true` |
| `POSTGRES_DB` | Nom de la base | `reports` |
| `POSTGRES_USER` | Utilisateur PostgreSQL | `reports` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `reports` |
| `REDIS_URL` | URL Redis | `redis://redis:6379/0` |
| `LLM_API_KEY` | Clé API OpenAI | — |
| `EMAIL_HOST` | Serveur SMTP | — |
| `EMAIL_IMAP_HOST` | Serveur IMAP (ingestion) | — |
| `FRONTEND_URL` | URL du frontend | `http://localhost:5173` |

## Structure du projet

```
.
├── backend/
│   ├── accounts/          # Auth JWT (register, login, me)
│   ├── config/            # Settings, URLs, Celery
│   ├── reports/
│   │   ├── management/commands/
│   │   ├── services/      # Parser, cleaner, charts, LLM, PDF, email, cache
│   │   ├── tests/         # 32 tests
│   │   ├── models.py
│   │   ├── views.py       # Dashboard, Upload, Stats, PDF
│   │   ├── tasks.py       # Celery pipeline
│   │   └── urls.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # Header, Layout, Charts, KPI, etc.
│   │   ├── contexts/      # AuthContext, ThemeContext
│   │   ├── pages/         # Landing, Login, Register, Upload, Reports, Analytics, Dashboard
│   │   ├── services/      # API client (auth, upload, polling)
│   │   └── index.css      # Design system complet
│   └── package.json
├── docker-compose.yml
└── PROMPT_PFE.md
```

## Équipe

| Membre | Rôle |
|--------|------|
| Chadi | Chef de projet / DevOps |
| Ayoub | Backend Django |
| Haitem | Frontend React |
| Moussa | IA / Data |
