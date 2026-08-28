# Guide de démonstration — Dashbail

## Préparation

1. Lancer la stack : `docker-compose up --build`
2. Attendre que tous les services soient UP
3. Ouvrir http://localhost:5173 dans le navigateur

## Étape 1 — Landing Page

- Montrer la page d'accueil avec le hero animé
- Scroll vers le bas : "Comment ça marche" (3 étapes), Fonctionnalités (6 cartes), Stack technique
- Cliquer sur "Commencer gratuitement"

## Étape 2 — Inscription

- Remplir le formulaire : nom d'utilisateur, email, mot de passe
- Cliquer sur "Créer mon compte"
- Vérifier la redirection vers la page d'accueil (utilisateur connecté)

## Étape 3 — Connexion alternative

- Se déconnecter via le menu utilisateur
- Se connecter avec les identifiants créés
- Vérifier que le Header affiche le nom d'utilisateur

## Étape 4 — Upload de fichier

- Cliquer sur "Analyser" dans la navigation
- Glisser un fichier CSV dans la zone de drop (ou cliquer pour parcourir)
- Entrer un titre optionnel
- Cliquer sur "Lancer l'analyse"
- Observer le status "En cours de traitement" avec le polling automatique

## Étape 5 — Dashboard interactif

- Le dashboard se charge automatiquement après le traitement
- Montrer les KPIs avec compteurs animés (de 0 à la valeur)
- Montrer les graphiques (bar, line) avec Recharts
- Montrer les insights IA avec code couleur (vert/rouge/neutre)
- Montrer le score de qualité des données

## Étape 6 — Partage

- Cliquer sur "Partager" dans le header du dashboard
- Vérifier le message "Lien copié !"
- Coller le lien dans un autre onglet pour montrer l'accessibilité publique

## Étape 7 — Historique

- Cliquer sur "Historique" dans la navigation
- Montrer la liste des rapports avec badges de statut
- Utiliser la recherche et les filtres
- Cliquer sur un rapport pour l'ouvrir

## Étape 8 — Analytics

- Cliquer sur "Analytics" dans la navigation
- Montrer les KPIs globaux (total, terminés, échoués, données traitées)
- Montrer le pie chart de répartition par statut
- Montrer le bar chart des lignes par rapport
- Montrer les 5 derniers rapports

## Étape 9 — Export PDF

- Ouvrir un rapport
- Cliquer sur le lien PDF dans le footer
- Ouvrir le PDF téléchargé pour montrer le contenu

## Étape 10 — Dark mode

- Cliquer sur le bouton 🌙 dans le Header
- Vérifier que toutes les pages basculent en mode sombre
- Montrer le contraste et la lisibilité
- Rebasculer en mode clair

## Étape 11 — Swagger API

- Ouvrir http://localhost:8000/api/docs/
- Montrer la documentation interactive de l'API
- Tester un endpoint directement depuis Swagger

## Étape 12 — Responsive

- Redimensionner la fenêtre en mode mobile (375px)
- Montrer le hamburger menu dans le Header
- Vérifier que toutes les pages sont utilisables sur mobile

## Données de test

5 rapports seed disponibles après `seed_data` :
1. Ventes Q1 2024 — 1250 lignes, 2 graphiques
2. Rapport Marketing Mars — 3200 lignes, 2 graphiques
3. Analyse RH - Effectifs 2024 — 480 lignes, 1 graphique
4. Performance Financière 2024 — 890 lignes, 1 graphique
5. Satisfaction Client T3 — 2100 lignes, 2 graphiques

## Points clés à souligner lors de la soutenance

1. **Architecture SaaS complète** — Backend Django + Celery + Redis + PostgreSQL
2. **Pipeline d'analyse IA** — Parsing → Cleaning → LLM → Génération de graphiques
3. **Frontend moderne** — React, Recharts, framer-motion, design system CSS
4. **Auth JWT** — Sécurité des données avec tokens
5. **API Swagger** — Documentation automatique
6. **Fallback intelligent** — LLM + heuristiques pour la robustesse
7. **42 tests** — Qualité logicielle
8. **Docker** — Déploiement containerisé
9. **Flux email sans compte** — Ingestion IMAP auto (Celery beat) + renvoi du lien par SMTP
10. **Dark mode** — UX moderne
11. **Responsive** — Compatible mobile/tablette
