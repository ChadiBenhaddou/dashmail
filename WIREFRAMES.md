# Wireframes — Dashboard Page

> Referentiel visuel pour l'implémentation React du dashboard Dashboard Bail.
>
> 4 etats documentes : Desktop (succes), Mobile, Loading, Error.
> Chaque etat inclut les noms de composants React pour guider l'implementation.

---

## Sommaire

1. [Desktop — Etat de succes](#1-desktop--etat-de-succes)
2. [Mobile — Vue responsive](#2-mobile--vue-responsive)
3. [Loading — Chargement](#3-loading--chargement)
4. [Error — Etat d'erreur](#4-error--etat-derreur)
5. [Carte des composants](#5-carte-des-composants)

---

## 1. Desktop — Etat de succes

### Layout general

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  HEADER                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ [Logo] Dashbail   [Badge PRO]   [📅 25 Aout 2026]   [Avatar]   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  REPORT HEADER CARD                                                 │    │
│  │  [Terminé ✓]  [Ventes]  [Q3 2026]                                  │    │
│  │                                                                     │    │
│  │  Rapport des ventes trimestriel                                     │    │
│  │  ventes_q3_2026.csv                                                 │    │
│  │  Synthese automatique generee le 25/08/2026 a 14:32                 │    │
│  │                                                                     │    │
│  │  📊 1 247 lignes analysees                     [⬇ Telecharger]     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  VUE D'ENSEMBLE — <ReportHeader />                                  │    │
│  │                                                                     │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │    │
│  │  │ Chiffre      │ │ Nb Clients   │ │ Commandes    │ │ Taux       │ │    │
│  │  │ d'affaires   │ │              │ │              │ │ conversion │ │    │
│  │  │              │ │              │ │              │ │            │ │    │
│  │  │ 248 500 EUR  │ │ 1 023        │ │ 3 412        │ │ 4.2%       │ │    │
│  │  │ ▲ +12.3%     │ │ ▲ +8.1%      │ │ ▼ -2.4%     │ │ ▲ +0.8%   │ │    │
│  │  │ vs last qtr  │ │ vs last qtr  │ │ vs last qtr  │ │ vs last qtr│ │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │    │
│  │                                                                     │    │
│  │  <KPICard /> x4                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  EVOLUTION DES VENTES — <SalesEvolutionChart />                     │    │
│  │                                                                     │    │
│  │  300K |                                                             │    │
│  │       |                          ╱╲                                 │    │
│  │  250K |                    ╱╲  ╱    ╲    ╱╲                         │    │
│  │       |              ╱╲  ╱    ╲╱      ╲╱    ╲                      │    │
│  │  200K |        ╱╲  ╱    ╲╱                      ╲                  │    │
│  │       |  ╱╲  ╱    ╲╱                                              │    │
│  │  150K |╱    ╲╱                                                     │    │
│  │       |                                                             │    │
│  │  100K +────────────────────────────────────────────────             │    │
│  │       Jan  Fev  Mar  Avr  Mai  Jun  Jul  Aou  Sep                  │    │
│  │                                                                     │    │
│  │  ─── 2026   ─ ─ 2025 (reference)                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  VENTES PAR REGION                                                  │    │
│  │                                                                     │    │
│  │  <RegionalBarChart />              ┌───────────────────────────┐    │    │
│  │                                    │  INSIGHT CARD             │    │    │
│  │  Ile-de-France  ████████████ 82K  │                           │    │    │
│  │  Auvergne-Rhone ██████████   67K  │  "L'Ile-de-France         │    │    │
│  │  Occitanie      ████████     54K  │   domine avec 33% du      │    │    │
│  │  Nouvelle-Aquit ████         28K  │   CA total, en hausse     │    │    │
│  │  Bretagne       ███          17K  │   de 15% vs T2."          │    │    │
│  │                                    │                           │    │    │
│  │                                    │  — Analyse IA             │    │    │
│  │                                    └───────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  RESUME INTELLIGENT — <SmartSummary />                              │    │
│  │                                                                     │    │
│  │  1. Le chiffre d'affaires a progresse de 12.3% ce trimestre,       │    │
│  │     porte par une forte hausse en Ile-de-France (+15%).             │    │
│  │                                                                     │    │
│  │  2. Le nombre de clients a augmente de 8.1%, signe d'une           │    │
│  │     bonne acquisition.                                              │    │
│  │                                                                     │    │
│  │  3. Le taux de conversion s'ameliore (+0.8 points) mais            │    │
│  │     le nombre de commandes a legerement baisse (-2.4%).             │    │
│  │                                                                     │    │
│  │  4. L'Ile-de-France concentre 33% du CA, suivi de                 │    │
│  │     l'Auvergne-Rhone-Alpes (27%).                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  QUALITE DES DONNEES — <DataQuality />                              │    │
│  │                                                                     │    │
│  │  Score global : 87/100                                              │    │
│  │  ┌──────────────────────────────────────────────────────────┐       │    │
│  │  │████████████████████████████████████████████░░░░░░░░░░░░░░│ 87%  │    │
│  │  └──────────────────────────────────────────────────────────┘       │    │
│  │                                                                     │    │
│  │  Completesse: 94%  |  Formats: 89%  |  Coherence: 78%             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  FOOTER — <Footer />                                                │    │
│  │  Dashboard Bail v0.1  |  Genere par IA  |  Contact support         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Composants Desktop

| Composant React | Role | Emplacement |
|-----------------|------|-------------|
| `<DashboardHeader />` | Barre superieure : logo, badge plan, date, avatar | Fixe en haut |
| `<ReportHeaderCard />` | Carte recapitulative du rapport : badges, titre, fichier, nb lignes, bouton telecharger | Sous le header |
| `<KPICard />` | Carte individuelle d'un KPI (valeur, tendance, reference) | Grille 4 colonnes |
| `<KPIGrid />` | Conteneur grille pour les 4 `<KPICard />` | Section "Vue d'ensemble" |
| `<SalesEvolutionChart />` | Graphique en courbes (evolution mensuelle, 2 annees) | Section "Evolution des ventes" |
| `<RegionalBarChart />` | Graphique en barres horizontales (ventes par region) | Colonne gauche |
| `<InsightCard />` | Carte de texte generee par l'IA (insight sur les regions) | Colonne droite |
| `<SmartSummary />` | Liste numerotee de syntheses IA | Section "Resume intelligent" |
| `<DataQuality />` | Score + barre de progression + metriques de qualite | Section "Qualite des donnees" |
| `<Footer />` | Pied de page : version, mention IA, contact | Bas de page |

### Styles Desktop

- **Largeur max contenu** : 1120px centre
- **Grille KPI** : `grid-template-columns: repeat(4, 1fr)`, gap 16px
- **Grille Region** : 2 colonnes (barres 60% / insight 40%), gap 24px
- **Cartes** : border-radius 12px, ombre `0 2px 8px rgba(0,0,0,0.06)`, padding 24px
- **Typographie** : titres 20-24px bold, KPI valeurs 28-32px bold, corps 14px

---

## 2. Mobile — Vue responsive

### Layout general (viewport < 768px)

```
┌─────────────────────────┐
│ HEADER (compact)        │
│ [≡] Dashbail  [Avatar]│
└─────────────────────────┘
┌─────────────────────────┐
│ REPORT HEADER CARD      │
│ [Terminé ✓] [Ventes]   │
│                         │
│ Rapport des ventes      │
│ trimestriel             │
│ ventes_q3_2026.csv      │
│ Synthese generee le     │
│ 25/08/2026 a 14:32      │
│                         │
│ 📊 1 247 lignes         │
│ [⬇ Telecharger]         │
└─────────────────────────┘
┌─────────────────────────┐
│ VUE D'ENSEMBLE          │
│ ┌─────────────────────┐ │
│ │ Chiffre d'affaires  │ │
│ │ 248 500 EUR ▲+12.3%│ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ Nb Clients          │ │
│ │ 1 023 ▲+8.1%       │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ Commandes           │ │
│ │ 3 412 ▼-2.4%       │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ Taux conversion     │ │
│ │ 4.2% ▲+0.8%        │ │
│ └─────────────────────┘ │
└─────────────────────────┘
┌─────────────────────────┐
│ EVOLUTION DES VENTES    │
│ ┌─────────────────────┐ │
│ │                     │ │
│ │  [Graphique simplifie│ │
│ │   4-6 points max,   │ │
│ │   axes reduits]     │ │
│ │                     │ │
│ └─────────────────────┘ │
│ ─── 2026  - - 2025     │
└─────────────────────────┘
┌─────────────────────────┐
│ VENTES PAR REGION       │
│ ┌─────────────────────┐ │
│ │ IDF  ████████  82K  │ │
│ │ AR   ██████    67K  │ │
│ │ Occ  █████     54K  │ │
│ │ NA   ███       28K  │ │
│ │ Bre  ██        17K  │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ INSIGHT CARD        │ │
│ │ "L'Ile-de-France    │ │
│ │  domine avec 33%    │ │
│ │  du CA..."          │ │
│ └─────────────────────┘ │
└─────────────────────────┘
┌─────────────────────────┐
│ RESUME INTELLIGENT      │
│                         │
│ 1. Le CA a progresse   │
│    de 12.3% ce trimestre│
│                         │
│ 2. Les clients ont      │
│    augmente de 8.1%     │
│                         │
│ 3. Conversion en        │
│    hausse mais commandes│
│    en leger recul       │
│                         │
│ 4. IDF = 33% du CA      │
└─────────────────────────┘
┌─────────────────────────┐
│ QUALITE DES DONNEES     │
│ Score : 87/100          │
│ ┌─────────────────────┐ │
│ │███████████████░░░░░░│ │
│ └─────────────────────┘ │
│ Compl: 94% | Fmt: 89%  │
│ Coh: 78%               │
└─────────────────────────┘
┌─────────────────────────┐
│ FOOTER                  │
│ Dashboard Bail v0.1     │
│ Genere par IA | Contact │
└─────────────────────────┘
```

### Differences Mobile vs Desktop

| Element | Desktop | Mobile |
|---------|---------|--------|
| `<DashboardHeader />` | Logo + badge + date + avatar en ligne | Logo + avatar seulement, badge/date masques |
| `<KPICard />` | 4 en grille horizontale | 1 par ligne, empiles verticalement |
| `<SalesEvolutionChart />` | 12 points (mensuel), 2 series | 6 points (bimensuel), 1 serie, tooltips natifs |
| `<RegionalBarChart />` + `<InsightCard />` | 2 colonnes cote a cote | Empiles, insight en dessous |
| `<SmartSummary />` | Texte long avec detail | Texte tronque, bouton "Voir plus" |
| `<DataQuality />` | 4 metriques en ligne | 2 colonnes, metriques empilees |
| Padding cartes | 24px | 16px |
| Border radius | 12px | 8px |

### Composants Mobile supplementaires

| Composant React | Role |
|-----------------|------|
| `<MobileNav />` | Bouton hamburger pour menu futur |
| `<KPICardCompact />` | Variante mobile du KPI (layout vertical) |

---

## 3. Loading — Chargement

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER (grise / inactive)                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ [Logo] Dashbail              [···]  [□]              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│                                                                 │
│                    ┌─────────────────────────┐                  │
│                    │                         │                  │
│                    │      ◌ (spinner)        │                  │
│                    │                         │                  │
│                    │  Chargement du rapport… │                  │
│                    │                         │                  │
│                    │  ─────────────────────  │                  │
│                    │                         │                  │
│                    │  ✅ Lecture du fichier  │                  │
│                    │     ↓                   │                  │
│                    │  ◌ Analyse des donnees  │                  │
│                    │     ↓                   │                  │
│                    │  ○ Generation du rapport│                  │
│                    │                         │                  │
│                    └─────────────────────────┘                  │
│                                                                 │
│                                                                 │
│                                                                 │
│                                                                 │
│  FOOTER (grise / inactive)                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Etapes du pipeline

```
  ✅ Lecture du fichier       Etape terminee (checkmark vert)
  ◌  Analyse des donnees      Etape en cours (spinner anime)
  ○  Generation du rapport    Etape en attende (cercle grise)
```

### Composants Loading

| Composant React | Role |
|-----------------|------|
| `<LoadingView />` | Conteneur principal de l'etat loading |
| `<LoadingSpinner />` | Animation spinner centree (CSS ou SVG) |
| `<StepPipeline />` | Affichage des 3 etapes avec etats visuels |
| `<StepItem />` | Une etape individuelle (icon + label + etat) |

### Animations

- **Spinner** : rotation CSS `360deg` infinie, 1.2s ease-in-out
- **Etape active** : pulse subtil sur le spinner local
- **Transition etapes** : when an step completes, checkmark fade-in 0.3s
- **Texte** : "Chargement du rapport…" avec animation points (...) cycle

### Etats du pipeline (etapes)

| Etat | Icone | Couleur | Animation |
|------|-------|---------|-----------|
| `completed` | Checkmark `✓` | Vert (#22c55e) | Fade-in |
| `active` | Spinner `◌` | Bleu primary (#3b82f6) | Rotation |
| `pending` | Cercle `○` | Gris (#9ca3af) | Aucune |

---

## 4. Error — Etat d'erreur

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER (grise / inactive)                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ [Logo] Dashbail              [···]  [□]              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│                                                                 │
│                    ┌─────────────────────────┐                  │
│                    │                         │                  │
│                    │     ⚠ (icone rose)      │                  │
│                    │                         │                  │
│                    │  Impossible de charger  │                  │
│                    │     ce rapport          │                  │
│                    │                         │                  │
│                    │  ─────────────────────  │                  │
│                    │                         │                  │
│                    │  Une erreur est survenue│                  │
│                    │  lors du chargement des │                  │
│                    │  donnees. Verifiez que  │                  │
│                    │  le rapport existe et   │                  │
│                    │  reessayez.             │                  │
│                    │                         │                  │
│                    │  ┌───────────────────┐  │                  │
│                    │  │    Réessayer       │  │                  │
│                    │  └───────────────────┘  │                  │
│                    │                         │                  │
│                    │      Fermer             │                  │
│                    │                         │                  │
│                    └─────────────────────────┘                  │
│                                                                 │
│                                                                 │
│                                                                 │
│  FOOTER (grise / inactive)                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Composants Error

| Composant React | Role |
|-----------------|------|
| `<ErrorView />` | Conteneur principal de l'etat erreur |
| `<ErrorIcon />` | Icone d'erreur stylisee (icone rose, SVG ou emoji) |
| `<RetryButton />` | Bouton "Reessayer" — reload du rapport |
| `<CloseLink />` | Lien "Fermer" — retour a la liste des rapports |

### Comportements

| Action | Comportement |
|--------|-------------|
| Clic "Reessayer" | Re-lance `fetchReport(id)`, passe en etat Loading |
| Clic "Fermer" | `navigate('/')` retour a la page d'historique |
| Refresh navigateur | Meme etat Error affiche (pas de cache) |

### Styles Error

- **Container** : `max-width: 420px`, center, padding 48px
- **Icone** : 64px, couleur `#f43f5e` (rose-500)
- **Titre** : 20px, bold, `#1f2937` (gray-800)
- **Description** : 14px, `#6b7280` (gray-500), line-height 1.6
- **Bouton Reessayer** : fond `#3b82f6`, texte blanc, border-radius 8px, padding 10px 24px
- **Lien Fermer** : texte `#6b7280`, sans decoration, underline au hover

---

## 5. Carte des composants

### Arborescence proposee dans `src/components/`

```
src/
├── components/
│   ├── DashboardHeader.jsx
│   ├── ReportHeaderCard.jsx
│   ├── kpi/
│   │   ├── KPICard.jsx
│   │   └── KPICardCompact.jsx
│   ├── KPIGrid.jsx
│   ├── charts/
│   │   ├── SalesEvolutionChart.jsx
│   │   └── RegionalBarChart.jsx
│   ├── InsightCard.jsx
│   ├── SmartSummary.jsx
│   ├── DataQuality.jsx
│   ├── Footer.jsx
│   ├── loading/
│   │   ├── LoadingView.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── StepPipeline.jsx
│   │   └── StepItem.jsx
│   └── error/
│       ├── ErrorView.jsx
│       ├── ErrorIcon.jsx
│       ├── RetryButton.jsx
│       └── CloseLink.jsx
├── pages/
│   └── ReportPage.jsx        ← Page principale, orchestre les 4 etats
├── hooks/
│   └── useReport.js          ← Hook : fetch report, gere loading/error/success
└── services/
    └── api.js                ← Client HTTP pour /api/reports/:id/
```

### Flux des etats dans ReportPage

```
                   useReport(id)
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
        Loading      Success      Error
            │           │           │
    <LoadingView/>  <Dashboard>  <ErrorView/>
    <StepPipeline/>  │          <ErrorIcon/>
            │       │           <RetryButton/>
            │       ├── <DashboardHeader/>
            │       ├── <ReportHeaderCard/>
            │       ├── <KPIGrid/>
            │       ├── <SalesEvolutionChart/>
            │       ├── <RegionalBarChart/> + <InsightCard/>
            │       ├── <SmartSummary/>
            │       ├── <DataQuality/>
            │       └── <Footer/>
```

### Hooks et services

| Fichier | Role |
|---------|------|
| `hooks/useReport.js` | Hook custom : `const { report, loading, error, refetch } = useReport(id)` |
| `services/api.js` | `fetchReport(id)`, `fetchReports()`, base URL depuis `VITE_API_BASE_URL` |
| `pages/ReportPage.jsx` | Route `/report/:id` — compose les 4 etats via le hook |

### Breakpoints responsive

| Breakpoint | Largeur | Comportement |
|------------|---------|-------------|
| `sm` | < 640px | Mobile strict, 1 colonne |
| `md` | 640-768px | Tablet compact, 2 colonnes KPI |
| `lg` | 768-1024px | Desktop compact, grille 3 colonnes |
| `xl` | > 1024px | Desktop large, grille 4 colonnes, layout 2 col region |
