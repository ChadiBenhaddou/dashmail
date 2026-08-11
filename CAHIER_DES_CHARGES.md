# Cahier des charges — Dashboard Bail

> Plateforme SaaS de génération de rapports visuels par email
>
> Version 1.0 — Document de référence pour le projet de fin d'année
> Équipe : Chadi (chef de projet / DevOps), Ayoub (backend Django), Haitem (frontend React), Moussa (IA / Data)

---

## Sommaire

1. [Présentation du projet](#1-présentation-du-projet)
2. [Objectifs](#2-objectifs)
3. [Utilisateurs cibles](#3-utilisateurs-cibles)
4. [Périmètre fonctionnel](#4-périmètre-fonctionnel)
5. [Architecture générale](#5-architecture-générale)
6. [Contraintes techniques](#6-contraintes-techniques)
7. [Contraintes non fonctionnelles](#7-contraintes-non-fonctionnelles)
8. [Critères de succès](#8-critères-de-succès)
9. [Jalons et planning](#9-jalons-et-planning)
10. [Risques et mitigations](#10-risques-et-mitigations)
11. [Hors périmètre](#11-hors-périmètre)

---

## 1. Présentation du projet

**Dashboard Bail** est une plateforme SaaS qui permet à des utilisateurs non techniques
d'obtenir automatiquement un **rapport visuel** (graphiques, indicateurs, synthèse) à
partir d'un fichier de données (**CSV / Excel**), **sans aucune manipulation complexe**.

Le parcours central est le suivant :

1. L'utilisateur envoie son fichier de données **par email** en pièce jointe.
2. La plateforme **ingère** le fichier, en **analyse** le contenu.
3. Un **LLM** identifie les colonnes, les tendances et les indicateurs clés.
4. La plateforme **génère un rapport visuel** (PDF ou HTML embarqué).
5. Le rapport est **renvoyé par email** à l'expéditeur.

Un **dashboard web** complète le dispositif pour consulter l'historique des rapports,
suivre l'état des traitements et gérer le compte.

---

## 2. Objectifs

### 2.1 Objectif général

Permettre à tout utilisateur d'obtenir un rapport visuel exploitable à partir d'un
simple email, en automatisant l'analyse des données grâce à l'IA.

### 2.2 Objectifs spécifiques

| # | Objectif | Mesure |
|---|----------|--------|
| O1 | Automatiser la génération de rapports à partir d'un email | Taux de rapports générés sans intervention humaine ≥ 90 % |
| O2 | Produire des rapports visuels lisibles et pertinents | Score de satisfaction utilisateur ≥ 4/5 |
| O3 | Offrir une expérience sans apprentissage technique | Temps de prise en main < 10 minutes |
| O4 | Garantir la fiabilité du pipeline (ingestion → rapport) | Taux de traitement réussi ≥ 95 % |
| O5 | Déployer une plateforme modulaire et extensible | Architecture validée par le dépôt Docker Compose |

---

## 3. Utilisateurs cibles

| Profil | Description | Besoins |
|--------|-------------|---------|
| **PME / TPE** | Petites entreprises sans data analyst, gérant leurs données dans Excel/CSV | Rapports simples et rapides à partir de fichiers existants |
| **Responsables commerciaux / marketing** | Suivent des indicateurs de vente ou de campagne | Synthèses périodiques (chiffres clés, tendances) |
| **Étudiants / chercheurs** | Besoin d'analyser rapidement un jeu de données | Visualisations rapides sans code |
| **Non-techniciens** | Utilisateurs ne sachant ni coder ni configurer un BI | Envoi d'un email = rapport reçu, sans autre action |

**Note :** l'utilisateur cible principal est **non technique**. Toute fonctionnalité
exigeant une compétence technique (SQL, script, config) est hors périmètre.

---

## 4. Périmètre fonctionnel

### 4.1 Fonctionnalités principales

#### F1 — Ingestion des données par email
- Réception des emails avec pièce(s) jointe(s) `.csv`, `.xlsx`, `.xls`.
- Vérification de l'expéditeur (adresse autorisée liée au compte).
- Limitation de la taille et du nombre de fichiers (voir §6.4).
- Sauvegarde brute du fichier et des métadonnées (expéditeur, sujet, date).
- Notification par email en cas de rejet (format, taille, expéditeur inconnu).

#### F2 — Analyse des données (LLM + pandas)
- Lecture et profilage du fichier avec **pandas** (types de colonnes, valeurs manquantes, doublons).
- **Prétraitement** : normalisation des en-têtes, détection des colonnes numériques, dates, catégories.
- **Inférence LLM** :
  - Détection de l'intention du fichier (ventes, RH, finance, stock…).
  - Choix des indicateurs pertinents (totaux, moyennes, évolutions, répartitions).
  - Génération de la synthèse rédigée en langage naturel.
- Génération d'un **schéma d'analyse reproductible** (JSON) stocké en base.

#### F3 — Génération du rapport visuel
- Construction des visualisations (barres, lignes, camemberts, histogrammes).
- Assemblage d'un rapport : indicateurs clés, graphiques, synthèse textuelle.
- Génération en format **HTML embarqué dans l'email** et/ou **PDF téléchargeable**.
- Template de rendu cohérent (marque, couleurs, hiérarchie d'information).

#### F4 — Livraison du rapport par email
- Renvoi automatique du rapport à l'expéditeur avec résumé en corps de message.
- Gestion des erreurs : renvoi d'un email d'explication si l'analyse échoue.
- Journalisation de la livraison (succès, échec, heure).

#### F5 — Dashboard web
- **Authentification** : inscription, connexion, gestion du profil.
- **Historique** : liste des rapports générés, statut (en attente, en cours, terminé, échec).
- **Consultation** : aperçu du rapport, téléchargement du PDF, visualisation dans le navigateur.
- **Upload manuel** : possibilité de déposer un fichier directement depuis l'interface (alternative à l'email).
- **Paramètres du compte** : adresses email autorisées, préférences de format (HTML/PDF).

#### F6 — Administration
- Interface d'admin Django pour gérer utilisateurs, rapports et tâches.
- Supervision des files Celery et des échecs de traitement.

### 4.2 Règles métier
- Un rapport est lié à un **compte** et à l'**expéditeur** de l'email.
- Un fichier non analysable → **email d'échec** avec explication, pas de blocage.
- Le LLM ne produit jamais de valeurs numériques ; tous les chiffres proviennent de **pandas**.
- Les données source sont **supprimées** après un délai configurable (RGPD).

---

## 5. Architecture générale

```
                    ┌──────────────────────────────────────────────┐
                    │                  FRONTEND (React)             │
                    │  Dashboard / Historique / Upload / Auth       │
                    └────────────────────┬─────────────────────────┘
                                         │ HTTP (API REST)
                    ┌────────────────────▼─────────────────────────┐
   Email ──────────►│                 BACKEND (Django)              │
  (CSV/XLSX)        │   API DRF   ·   Modèles   ·   Intégration     │
                    │   email entrant (IMAP)  ·   envoi SMTP        │
                    └────────────────────┬─────────────────────────┘
                                         │ tâches asynchrones
                    ┌────────────────────▼─────────────────────────┐
                    │         CELERY WORKER  (files d'attente)      │
                    │  Parsing CSV   ·   pandas   ·   Appel LLM     │
                    │  Génération graphes   ·   Rendu rapport       │
                    └────────────────────┬─────────────────────────┘
                                         │
          ┌──────────────┬───────────────┼──────────────┐
          ▼              ▼               ▼              ▼
     PostgreSQL      Redis         Stockage       Service LLM
      (données)      (broker)       fichiers       (API externe)
```

### 5.1 Flux de traitement nominal

1. Email reçu (daemon d'ingestion) → création d'une tâche Celery `ingest_email`.
2. Le worker valide l'expéditeur et le format du fichier.
3. pandas profile le fichier → `DataFrame` validé.
4. Prompt structuré envoyé au LLM → `analyse_schema` (JSON).
5. Calculs pandas + tracés → `rapport` (HTML/PDF).
6. Envoi SMTP du rapport + enregistrement en base.
7. Mise à jour du statut consultable dans le dashboard.

### 5.2 Répartition des rôles techniques

| Rôle | Responsabilité |
|------|----------------|
| **Backend (Django)** | API REST, modèles, auth, orchestration Celery, SMTP/IMAP |
| **Celery + Redis** | Exécution asynchrone, reprise sur erreur, scalabilité |
| **PostgreSQL** | Persistance : utilisateurs, rapports, métadonnées, schémas d'analyse |
| **pandas** | Traitement tabulaire fiable, calculs, validation |
| **LLM** | Compréhension sémantique, choix d'indicateurs, rédaction synthèse |
| **React** | Interface utilisateur du dashboard |

---

## 6. Contraintes techniques

### 6.1 Backend — Django

| Contrainte | Exigence |
|------------|----------|
| Version | Django ≥ 5.0, Django REST Framework ≥ 3.15 |
| Asynchrone | Celery ≥ 5.4, broker Redis ≥ 5.0 |
| Base de données | PostgreSQL (via `psycopg2`) |
| Traitement données | pandas ≥ 2.2 |
| Configuration | Env séparés `dev` / `prod` (`config/settings/`) |
| API | REST, authentification par session (démarrage) → JWT en production |
| Validation | Sérialiseurs DRF stricts, limites de taille/type fichiers |

### 6.2 Frontend — React

| Contrainte | Exigence |
|------------|----------|
| Version | React 18, build Vite ≥ 5 |
| Routage | React Router v6 |
| Style | CSS modulaire, design cohérent avec le rapport |
| API | Client HTTP centralisé (`src/services`), hooks React (`src/hooks`) |
| Compatibilité | Navigateurs récents (Chrome, Firefox, Edge, Safari) |
| Responsive | Dashboard utilisable sur desktop et tablette |

### 6.3 LLM — IA / Data

| Contrainte | Exigence |
|------------|----------|
| Fournisseur | API LLM externe (clé configurable `LLM_API_KEY`) |
| Format échange | Prompt structuré → sortie **JSON validée** (schéma) |
| Souveraineté des chiffres | Le LLM ne calcule **jamais** de statistique ; pandas reste la source de vérité |
| Dégradation | Si l'appel LLM échoue → fallback sur règles heuristiques (types + indicateurs par défaut) |
| Coût | Limitation du nombre de tokens (résumé des données, pas d'envoi brut si gros fichier) |
| Sécurité du prompt | Échappement du contenu utilisateur pour prévenir l'injection de prompt |

### 6.4 Email

| Contrainte | Exigence |
|------------|----------|
| Ingestion | Protocole IMAP, polling périodique, dossier dédié |
| Envoi | SMTP avec TLS/SSL, `EMAIL_FROM` dédié |
| Formats acceptés | `.csv`, `.xlsx`, `.xls` — autres formats rejetés |
| Taille max | 20 Mo par email, 3 pièces jointes max |
| Anti-abuse | Seuls les expéditeurs autorisés déclenchent un traitement |

### 6.5 Conteneurs / Déploiement

- Déploiement Docker Compose : `postgres`, `redis`, `backend`, `celery_worker`, `frontend`.
- Configuration 100 % par variables d'environnement (`backend` : `DJANGO_*`, `POSTGRES_*`, `REDIS_URL`, `LLM_API_KEY`, `EMAIL_*` ; `frontend` : `VITE_API_BASE_URL`).
- Un fichier `.env.example` documente toutes les variables.
- Volumes nommés pour la persistance PostgreSQL.
- Santé des services vérifiée par healthchecks (pg_isready, redis-cli ping).

---

## 7. Contraintes non fonctionnelles

| Catégorie | Exigence |
|-----------|----------|
| **Performance** | Rapport moyen généré en < 5 min ; dashboard chargé en < 3 s |
| **Disponibilité** | 95 % en phase de démonstration ; file d'attente résiliente aux redémarrages |
| **Sécurité** | Clés en env vars, jamais en clair dans le dépôt ; CORS restreint ; validation des fichiers (type, taille, contenu) ; protection contre injection de prompt |
| **Confidentialité (RGPD)** | Données traitées à des fins uniquement fonctionnelles ; suppression des fichiers bruts après délai configurable |
| **Maintenabilité** | Code structuré par couches (modèles, services, vues, tâches) ; app Django `reports` dédiée |
| **Traçabilité** | Statut et logs de chaque rapport (soumission, traitement, livraison) |
| **Tests** | Tests unitaires backend (modèles, sérialiseurs, tâches) ; tests des pipelines de données |

---

## 8. Critères de succès

### 8.1 Critères fonctionnels

| # | Critère | Cible |
|---|---------|-------|
| CS1 | Un fichier envoyé par email produit un rapport | ≥ 95 % des emails valides |
| CS2 | Le rapport contient graphiques + chiffres + synthèse | 100 % des rapports générés |
| CS3 | L'expéditeur reçoit le rapport sans action supplémentaire | 100 % des traitements réussis |
| CS4 | Le dashboard affiche l'état temps réel des rapports | 100 % (interrogation du statut) |
| CS5 | Upload manuel depuis le dashboard fonctionne | Test de bout en bout validé |

### 8.2 Critères techniques

| # | Critère | Cible |
|---|---------|-------|
| CT1 | Pipeline complet déployé via `docker-compose up` | Sans erreur sur machine vierge |
| CT2 | Les 5 services sont sains (healthchecks) | 100 % |
| CT3 | Tests backend exécutés sans erreur | 100 % de réussite |
| CT4 | Aucun secret en clair dans le dépôt | Audit du dépôt |
| CT5 | Résilience : panne LLM → fallback fonctionnel | Scénario de test passé |

### 8.3 Critères de démonstration

- 1 fichier CSV de démonstration → rapport complet en < 5 min.
- 1 scénario d'échec (mauvais format) → email explicatif reçu.
- Dashboard navigable avec 5 rapports d'historique minimum.

---

## 9. Jalons et planning

| Jalon | Contenu | Livrable |
|-------|---------|----------|
| **J1 — Socle** | Dépôt, Docker Compose, settings dev/prod, CI minimale | Stack 5 services démarre |
| **J2 — Ingestion** | Modèles, réception email, upload manuel, tâche d'ingestion | Fichier stocké + statut « en cours » |
| **J3 — Analyse** | Profilage pandas, prompt LLM, validation du schéma JSON | Schéma d'analyse généré |
| **J4 — Rapport** | Graphes, rendu HTML/PDF, envoi SMTP, email de réception | Rapport complet livré par email |
| **J5 — Dashboard** | Auth, historique, consultation, téléchargement | Plateforme utilisable de bout en bout |
| **J6 — Qualité** | Tests, fallback LLM, anti-injection, RGPD | Critères de succès vérifiés |
| **J7 — Démo** | Données de démo, script de scénario, soutenance | Soutenance réussie |

---

## 10. Risques et mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Données CSV hétérogènes / sales | Moyen | Nettoyage pandas + heuristiques + rejet explicite |
| Hallucination du LLM sur les chiffres | Élevé | Les chiffres viennent uniquement de pandas ; le LLM ne génère que texte et choix d'indicateurs |
| Panne / quota LLM | Moyen | Fallback heuristique + file Celery avec retry |
| Fichiers volumineux | Moyen | Limites de taille, streaming, résumé des données pour le LLM |
| Injection de prompt via le fichier | Élevé | Échappement du contenu, instructions strictes, sortie JSON validée |
| Indisponibilité SMTP/IMAP | Moyen | File de messages, retries Celery, alertes logs |
| Dérive de calendrier (PFA) | Moyen | Jalons courts, MVP strict d'abord, fonctionnalités bonus ensuite |

---

## 11. Hors périmètre

- Analyse temps réel / streaming de données.
- Éditeur de rapports drag & drop (BI type Power BI).
- Programmation automatique de rapports récurrents (abandonné au MVP, possible en V2).
- Connecteurs vers des bases de données externes (SQL, ERP, CRM).
- Application mobile native (le dashboard web est responsive).
- Multilinguisme avancé (français en V1).
- Facturation / gestion des abonnements (V2).
