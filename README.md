# Dashboard X

Plateforme SaaS de **generation automatique de rapports visuels** a partir de
fichiers **CSV / Excel** envoyes par **email**.

## Architecture

| Couche           | Technologie                                                      |
| ---------------- | ---------------------------------------------------------------- |
| Backend          | Django + Django REST Framework + Celery + Redis + PostgreSQL     |
| Frontend         | React 18 (Vite) + Recharts                                      |
| LLM              | OpenAI GPT-4o                                                    |
| Conteneurisation | Docker + docker-compose                                         |

## Fonctionnalites

- Envoi de fichiers CSV/Excel par email
- Analyse automatique des donnees avec pandas
- Generation de visualisations par IA (Recharts)
- Dashboard interactif accessible sans compte via lien unique
- Email de notification (succes / echec)

## Installation locale

### Pre-requis

- [Docker](https://www.docker.com/) et Docker Compose
- Cle API OpenAI

### Etapes

1. Cloner le depot :

   ```bash
   git clone <repository-url> dashbail
   cd dashbail
   ```

2. Copier `.env.example` en `.env` et renseigner les variables :

   ```bash
   cp .env.example .env
   ```

3. Lancer la stack :

   ```bash
   docker-compose up --build
   ```

4. Creer un superuser :

   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. Charger les donnees de test :

   ```bash
   docker-compose exec backend python manage.py seed_data
   ```

### Acces aux services

| Service   | URL                           |
| --------- | ----------------------------- |
| Frontend  | http://localhost:5173         |
| Backend   | http://localhost:8000         |
| Admin     | http://localhost:8000/admin/  |
| Postgres  | localhost:5432                |
| Redis     | localhost:6379                |

## Variables d'environnement

| Variable                | Description                                   | Defaut                      |
| ----------------------- | --------------------------------------------- | --------------------------- |
| `DJANGO_SECRET_KEY`     | Cle secrete Django                            | `change-me-in-production`   |
| `DJANGO_DEBUG`          | Mode debug                                    | `true`                      |
| `DJANGO_ALLOWED_HOSTS`  | Hosts autorises (separes par virgules)        | `*`                         |
| `POSTGRES_DB`           | Nom de la base de donnees                     | `reports`                   |
| `POSTGRES_USER`         | Utilisateur PostgreSQL                        | `reports`                   |
| `POSTGRES_PASSWORD`     | Mot de passe PostgreSQL                       | `reports`                   |
| `POSTGRES_HOST`         | Host PostgreSQL                               | `postgres`                  |
| `POSTGRES_PORT`         | Port PostgreSQL                               | `5432`                      |
| `REDIS_URL`             | URL de connexion Redis (Celery + cache)       | `redis://redis:6379/0`      |
| `LLM_API_KEY`           | Cle API OpenAI pour l'analyse LLM             | —                           |
| `EMAIL_HOST`            | Serveur SMTP sortant                          | —                           |
| `EMAIL_PORT`            | Port SMTP                                     | `587`                       |
| `EMAIL_HOST_USER`       | Utilisateur SMTP                              | —                           |
| `EMAIL_HOST_PASSWORD`   | Mot de passe SMTP                             | —                           |
| `EMAIL_USE_TLS`         | TLS pour le SMTP                              | `true`                      |
| `EMAIL_FROM`            | Adresse d'expediteur des emails               | `reports@example.com`       |
| `EMAIL_IMAP_HOST`       | Serveur IMAP (ingestion emails)               | —                           |
| `EMAIL_IMAP_PORT`       | Port IMAP                                     | `993`                       |
| `EMAIL_IMAP_USER`       | Utilisateur IMAP                              | —                           |
| `EMAIL_IMAP_PASSWORD`   | Mot de passe IMAP                             | —                           |
| `VITE_API_BASE_URL`     | URL du backend pour le frontend               | `http://localhost:8000`     |
| `FRONTEND_URL`          | URL du frontend (pour les emails)             | `http://localhost:5173`     |

## API Endpoints

| Endpoint                        | Methode | Description                              |
| ------------------------------- | ------- | ---------------------------------------- |
| `/api/reports/`                 | GET     | Liste des rapports (auth requise)        |
| `/api/reports/`                 | POST    | Creer un rapport (auth requise)          |
| `/api/reports/{id}/`            | GET     | Detail d'un rapport (auth requise)       |
| `/api/dashboard/<uuid>/`        | GET     | Donnees du dashboard (public)            |
| `/admin/`                       | GET     | Interface d'administration Django        |

## Structure du projet

```
.
├── backend/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── celery.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── reports/
│   │   ├── management/commands/
│   │   │   ├── seed_data.py
│   │   │   └── check_emails.py
│   │   ├── services/
│   │   │   ├── data_parser.py
│   │   │   ├── data_cleaner.py
│   │   │   ├── chart_generator.py
│   │   │   ├── llm_service.py
│   │   │   ├── llm_prompt.py
│   │   │   ├── email_ingestion.py
│   │   │   ├── email_notifier.py
│   │   │   ├── cache_service.py
│   │   │   ├── error_handler.py
│   │   │   └── monitoring.py
│   │   ├── tests/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartRenderer.jsx
│   │   │   ├── DataQuality.jsx
│   │   │   ├── ErrorState.jsx
│   │   │   ├── InsightList.jsx
│   │   │   ├── KPICard.jsx
│   │   │   ├── LoadingState.jsx
│   │   │   └── ReportHeader.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   └── NotFoundPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── Procfile
├── .env.example
└── README.md
```

## Developpement

### Backend

- **Models** : `backend/reports/models.py`
- **Views** : `backend/reports/views.py`
- **Tasks Celery** : `backend/reports/tasks.py`
- **Services** : `backend/reports/services/` (parser, cleaner, chart_generator, llm_service, email)

### Frontend

- **Components** : `frontend/src/components/`
- **Pages** : `frontend/src/pages/`
- **API client** : `frontend/src/services/api.js`

### Commandes utiles

```bash
# Logs d'un service
docker-compose logs -f backend

# Migrations
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Creer un superuser
docker-compose exec backend python manage.py createsuperuser

# Lancer le worker Celery
docker-compose up -d celery_worker

# Arreter la stack
docker-compose down

# Arreter et supprimer les donnees
docker-compose down -v
```

## Tests

```bash
cd backend && python manage.py test
```

## Deploiement

### Railway / Heroku

Le `Procfile` est inclus a la racine du projet :

```
web: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
worker: cd backend && celery -A config worker -l info
```

Activez les variables d'environnement dans `.env` avec `DJANGO_SETTINGS_MODULE=config.settings.prod`.

### Docker (production)

```bash
docker-compose -f docker-compose.yml up --build -d
```

## Equipe

| Membre   | Role                     |
| -------- | ------------------------ |
| Chadi    | Chef de projet / DevOps  |
| Ayoub    | Backend Django           |
| Haitem   | Frontend React           |
| Moussa   | IA / Data                |
