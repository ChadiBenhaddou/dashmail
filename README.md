# Dashboard Bail — CSV Report SaaS

Plateforme SaaS de **génération automatique de rapports visuels** à partir de
fichiers **CSV / Excel** envoyés par **email**. L'utilisateur envoie son fichier,
la plateforme l'analyse (IA/LLM), génère un rapport visuel et le renvoie.

## Équipe & rôles

| Membre  | Rôle                     |
| ------- | ------------------------ |
| Chadi   | Chef de projet / DevOps  |
| Ayoub   | Backend Django           |
| Haitem  | Frontend React           |
| Moussa  | IA / Data                |

## Stack technique

| Couche          | Technologie                                        |
| --------------- | -------------------------------------------------- |
| Backend         | Django + Django REST Framework + Celery            |
| File d'attente  | Celery / Redis                                     |
| Base de données | PostgreSQL                                         |
| Frontend        | React 18 + Vite + React Router                     |
| IA / Data       | LLM pour l'analyse + pandas                        |
| Conteneurs      | Docker Compose (backend, celery_worker, redis, postgres, frontend) |

## Structure du dépôt

```
.
├── backend/               # Django (config/, reports/, manage.py)
├── frontend/              # React + Vite (src/components, pages, hooks, services)
├── docker-compose.yml     # 5 services : backend, celery_worker, redis, postgres, frontend
├── .env.example           # Variables d'environnement (DB, REDIS, LLM, EMAIL)
└── README.md
```

## Installation locale

Prérequis : [Docker](https://www.docker.com/) et Docker Compose.

1. Cloner le dépôt :

   ```bash
   git clone <repository-url> dashbail
   cd dashbail
   ```

2. (Optionnel) Copier les variables d'environnement et les adapter :

   ```bash
   cp .env.example .env
   ```

3. Lancer la stack complète :

   ```bash
   docker-compose up --build
   ```

4. Accéder aux services :

   | Service  | URL                                  |
   | -------- | ------------------------------------ |
   | Frontend | http://localhost:5173                |
   | Backend  | http://localhost:8000                |
   | Admin    | http://localhost:8000/admin/         |
   | Postgres | localhost:5432                       |
   | Redis    | localhost:6379                       |

   > Sans `.env`, des valeurs par défaut de développement sont utilisées
   > (voir `docker-compose.yml`).

## Commandes utiles

```bash
# Logs d'un service
docker-compose logs -f backend

# Exécuter des commandes dans le backend
docker-compose exec backend python manage.py makemigrations

# Consommer les tâches Celery en tâche de fond
docker-compose up --build -d celery_worker

# Arrêter la stack
docker-compose down

# Arrêter la stack et supprimer les données (volume postgres)
docker-compose down -v
```

## Développement

- **Backend** : les sources sont montées dans le conteneur (`./backend:/app`)
  → live-reload de Django (`runserver`) et de Celery (`--reload` non activé,
  restart manuel).
- **Frontend** : les sources sont montées (`./frontend:/app`) → HMR de Vite
  activé (`usePolling` pour Docker sous Windows/Mac).
