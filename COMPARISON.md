# Comparaisons techniques — Phase 1

> Document de decision pour les choix techniques du projet Dashboard Bail.
>
> Three domaines analyses : fournisseurs LLM, bibliotheques de graphiques React, hebergement.

---

## Sommaire

1. [Fournisseurs LLM](#1-fournisseurs-llm)
2. [Bibliotheques de graphiques React](#2-bibliotheques-de-graphiques-react)
3. [Hebergement](#3-hebergement)

---

## 1. Fournisseurs LLM

### Critere de comparaison

| Critere | OpenAI (GPT-4o) | Mistral (Mistral Large) | Claude API (Claude 3.5 Sonnet) |
|---------|-----------------|------------------------|-------------------------------|
| **Cout / 1M tokens input** | 2.50 USD | 2.00 EUR (~2.20 USD) | 3.00 USD |
| **Cout / 1M tokens output** | 10.00 USD | 6.00 EUR (~6.60 USD) | 15.00 USD |
| **Facilite d'integration** | API REST simple, SDK Python officiel, tres documentee, large communaute | API REST compatible OpenAI, SDK Python `mistralai`, doc claire | API REST, SDK Python `anthropic`, doc de qualite |
| **Qualite sortie JSON** | Excellente — mode `response_format: json_object` natif, fiable pour schemas structures | Bonne — supporte JSON mode, mais moins fiable sur gros schemas complexes | Tres bonne — suit bien les schemas, mais pas de mode JSON natif (rely sur le prompt) |
| **Support francais** | Excellent — GPT-4o gere le francais couramment, generation de texte naturel fluide | Excellent — Mistral est une entreprise francaise, le francais est une langue native du modele | Bon — Claude supporte le francais mais est entraill principalement sur anglais |
| **Limite contexte** | 128K tokens | 128K tokens | 200K tokens |
| **Vitesse reponse** | Rapide (~2-5s pour une analyse) | Rapide (~2-4s) | Moyen-rapide (~3-6s) |
| **Disponibilite API** | Tres bonne (99.9%) | Bonne (occasionnellement des ralentisseurs) | Tres bonne (99.9%) |
| **Modeles disponibles** | gpt-4o, gpt-4o-mini, gpt-4-turbo | mistral-large, mistral-medium, mistral-small | claude-3.5-sonnet, claude-3-opus |

### Details d'analyse

#### OpenAI (GPT-4o)

**Avantages :**
- Documentation massive, tutoriels pour tous les cas d'usage
- Mode JSON natif (`response_format`) —ideal pour notre schema d'analyse
- Bilibliotheque `openai` Python tres simple d'utilisation
- Supporte le system prompt pour guider le comportement
- Integration facile avec pandas (resume de DataFrame en texte)

**Inconvenients :**
- C/output le plus eleve pour les longues syntheses
- Dependence forte vers OpenAI (proprietaire)

**Exemple d'appel :**
```python
from openai import OpenAI
client = OpenAI(api_key=LLM_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "Analyse ce DataFrame et retourne un JSON..."},
        {"role": "user", "content": dataframe_summary}
    ]
)
```

#### Mistral (Mistral Large)

**Avantages :**
- Entreprise europeenne (France) — souverainete des donnees
- Couts competitifs, prix en EUR (pas de conversion)
- API compatible OpenAI — migration facile
- Excellente maitrise du francais
- Bon rapport qualite/prix

**Inconvenients :**
- Communaute et documentation plus petites qu'OpenAI
- Disponibilite API parfois irreguliere en periode de forte charge
- Mode JSON moins robuste que GPT-4o sur schemas complexes

**Exemple d'appel :**
```python
from mistralai import Mistral
client = Mistral(api_key=LLM_API_KEY)

response = client.chat.complete(
    model="mistral-large-latest",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "Analyse ce DataFrame..."},
        {"role": "user", "content": dataframe_summary}
    ]
)
```

#### Claude API (Claude 3.5 Sonnet)

**Avantages :**
- Contexte tres large (200K tokens) — peut accepter de gros resumes
- Excellente comprehension de documents complexes
- Bons resultats sur les taches d'analyse et de synthese
- Contribution responsable (limites d'usage)

**Inconvenients :**
- Pas de mode JSON natif — depend du system prompt
- C/output le plus eleve (15 USD/1M tokens)
- SDK Python `anthropic` moins repandu
- Moins bon que GPT-4o pour le francais dans un contexte commercial
- Integration moinsDocumentee que OpenAI

**Exemple d'appel :**
```python
from anthropic import Anthropic
client = Anthropic(api_key=LLM_API_KEY)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Analyse ce DataFrame et retourne un JSON..."}
    ]
)
```

### Recommandation

**Choix : OpenAI (GPT-4o)**

**Justification :**
1. **Mode JSON natif** : Notre pipeline depend d'un schema JSON valide (analyse, indicateurs, synthese). Le `response_format: json_object` d'OpenAI est le plus fiable pour garantir une sortie structuree.
2. **Documentation et communaute** : En cas de probleme, la documentation OpenAI et la communaute sont inegalees — crucial pour un projet academique avec des delais.
3. **Support francais** : GPT-4o genere un francais de qualite professionnelle, necessaire pour les rapports destines a des utilisateurs francais.
4. **Cout total** : Pour notre usage (environ 50-100 rapports/jour, 1K tokens input + 2K tokens output par rapport), le cout est d'environ **1.50-3.00 USD/jour**, soit ~45-90 USD/mois — acceptable.

**Plan B** : Si le cout devient un facteur bloquant ou si la souverainete europeenne devient une exigence, migrer vers Mistral (compatible OpenAI, meme syntaxe).

---

## 2. Bibliotheques de graphiques React

### Critere de comparaison

| Critere | Chart.js | Recharts | D3.js |
|---------|----------|----------|-------|
| **Facilite d'utilisation** | Elevee — syntaxe declarative, configuration par objets | Elevee — composants React natifs, JSX intuitif | Faible — API imperative, necessite de nombreuses lignes de code |
| **Integration React** | Via `react-chartjs-2` (wrapper) — bon mais pas natif | **Natif React** — composes JSX, hooks, props | Pas d'integration React native — necessite `useRef` + `useEffect` + manipulation DOM |
| **Customisation** | Bonne — plugins pour extensions, mais limites sur les cas avances | Bonne — composants composites, customisation via props et render props | Excellente — controle total sur chaque element SVG/Canvas |
| **Bundle size** | ~60 KB (chart.js + auto-registration) | ~45 KB (tree-shakeable, import selectif) | ~250 KB ( complet, non tree-shakeable facilement) |
| **Types de graphiques** | Courbes, barres, pie, radar, doughnut, scatter | Courbes, barres, pie, area, radar, scatter, treemap | Tout (theoriquement) — mais a construire soi-meme |
| **Performance** | Bonne — Canvas 2D, rapide pour <1000 points | Bonne — SVG, peut ralentir >5000 points | Excellente — optimisee pour de gros jeux de donnees |
| **Animation** | Integree, fluide | Integree, fluide | A configurer manuellement |
| **Documentation** | Excellente, tres ancienne (mature) | Bonne, exemples nombreux | Excellente mais orientee non-React |
| **Maintenance** | Active (Chart.js 4.x) | Active (Recharts 2.x) | Active mais D3 est une bibliotheque generique |
| **Taille communaute** | Tres large (200K+ GitHub stars) | Large (23K+ GitHub stars) | Tres large (109K+ GitHub stars) |

### Details d'analyse

#### Chart.js + react-chartjs-2

**Avantages :**
- API simple : un objet `data` + un objet `options`
- `react-chartjs-2` fournit des composants React (`<Line>`, `<Bar>`, etc.)
- Beaucoup de plugins (zoom, annotation, datalabels)
- Canvas 2D — performances stables

**Inconvenients :**
- Pas natif React — c'est un wrapper autour d'une bibliotheque Canvas
- Customisation avancee complexe (pas de render props)
- Le wrapper peut avoir des bugs avec les mises a jour React strict mode
- Moins intuitif pour des layouts composes (ex: barres + insight a cote)

**Exemple :**
```jsx
import { Line } from 'react-chartjs-2';

const data = {
  labels: ['Jan', 'Fev', 'Mar', 'Avr'],
  datasets: [{
    label: 'Ventes 2026',
    data: [150, 200, 180, 250],
    borderColor: '#3b82f6',
  }]
};

function SalesChart() {
  return <Line data={data} options={{ responsive: true }} />;
}
```

#### Recharts

**Avantages :**
- **Natif React** : chaque element est un composant React (`<Line>`, `<XAxis>`, `<Tooltip>`)
- JSX declaratif : le graphique se lit comme du HTML
- Composants composes : `<ResponsiveContainer>`, `<AreaChart>`, `<BarChart>`
- Tree-shakeable : importez uniquement ce que vous utilisez
- Documentation avec exemples interactifs React
- Customisation via render props (`content` prop sur `<Tooltip>`, `<Label>`)

**Inconvenients :**
- SVG uniquement — peut etre lent >5000 points (pas notre cas)
- Moins de plugins que Chart.js
- Quelques limitations sur les graphiques tres complexes

**Exemple :**
```jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', sales: 150 },
  { month: 'Fev', sales: 200 },
  { month: 'Mar', sales: 180 },
  { month: 'Avr', sales: 250 },
];

function SalesChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="sales" stroke="#3b82f6" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

#### D3.js

**Avantages :**
- Controle total — chaque pixel est configurable
- Performances optimales pour de gros datasets
- Grille de calcul/integration tres puissante
- Standard de l'industrie pour la visualisation data

**Inconvenients :**
- **Pas React** : D3 manipule le DOM directement, entre en conflit avec React
- Code imperatif : 100+ lignes pour un graphique simple
- Courbe d'apprentissage tres raide
- Bundle size important (250 KB)
- Maintenance : dans notre contexte (PFA, delai court), c'est un risque majeur

**Exemple :**
```jsx
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function SalesChart({ data }) {
  const ref = useRef();

  useEffect(() => {
    const svg = d3.select(ref.current);
    // 50+ lignes de code pour dessiner un simple graphique en courbes...
  }, [data]);

  return <svg ref={ref} width={600} height={300} />;
}
```

### Recommandation

**Choix : Recharts**

**Justification :**
1. **Integration React native** : Recharts est concu pour React. Pas de wrapper, pas de conflit DOM. Chaque composant est un composant React avec des props.
2. **Facilite de maintenance** : Dans le cadre d'un PFA avec 4 developpeurs, la lisibilite du code est critique. Recharts se lit comme du JSX standard.
3. **Bundle size** : 45 KB tree-shakeable, le plus compact des 3 options.
4. **Suffisant pour nos besoins** : Courbes, barres, pie — Recharts couvre 100% de nos cas d'usage sans necessiter de customisation avancee.
5. **ResponsiveContainer** : Integration native avec le layout responsive du dashboard.

**Installation :**
```bash
npm install recharts
```

---

## 3. Hebergement

### Critere de comparaison

| Critere | Railway | Heroku | Scaleway |
|---------|---------|--------|----------|
| **Prix de base** | 5 USD/mois (starter) + usage | 7 USD/mois (basic dyno) + usage | 7.99 EUR/mois (DEV1-M) + usage |
| **Docker deploy** | Excellent — detection automatique du Dockerfile, deploiement natif | Bon — supporte les Dockerfiles via `heroku.yml`, mais natif Heroku Buildpacks | Bon — supporte les containers, mais deploiement via CLI ou API Scaleway |
| **PostgreSQL** | Natif — addon Railway Postgres, connection interne, zero config | Natif — Heroku Postgres addon, bien integre mais couteux en production | Natif — Scaleway Managed PostgreSQL, performant, en EU |
| **Free tier** | **Oui** — 5 USD de credits/mois (suffisant pour dev), pas de dynos limites | **Non** — heroku-eco (5 USD/mois) ou heroku-basic, plus de free tier depuis 2022 | **Oui** — 100 EUR de credits pour les 3 premiers mois, apres payant |
| **Redis** | Natif — addon Redis, meme reseau que le backend | Natif — Heroku Redis, bon mais couteux | Natif — Scaleway Managed Redis |
| **Deploiement git** | Push via `railway up` ou GitHub Actions | Push via `git push heroku main` | Push via Git + webhook ou CI/CD |
| **Logs et monitoring** | Dashboard integré, logs temps reel, metrics | Dashboard Heroku, logs via CLI | Console Scaleway, logs via API |
| **Limites free/starter** | 512 MB RAM, 1 vCPU (starter) | 512 MB RAM, 1 dyno | DEV1-M : 2 vCPU, 2 GB RAM |
| **Latence (EU)** | Bonne (serveurs US et EU) | Moyenne (principalement US) | **Excellente** (Paris, France) |
| **Scaling** | Auto-scale, scale a la demande | Manuel ou auto (payant) | Manuel via API ou console |
| **Souverainete donnees** | US (principalement) | US | **France (Paris)** |

### Details d'analyse

#### Railway

**Avantages :**
- Deploiement Docker extremement simple — un `Dockerfile` suffit
- Addons natifs : PostgreSQL, Redis, variables d'env
- GitHub integration : deploiement auto sur push
- Dashboard elegant avec logs, metrics, variables d'env
- 5 USD de credits gratuits/mois — suffisant pour le developpement

**Inconvenients :**
- Pas d'EU data center (principalement US) — potentiel RGPD
- Le free tier est un credit, pas un tier permanent
- En cas de depassement, facturation surprise possible

#### Heroku

**Avantages :**
- Tres documente, references universelles
- Addons matures (Postgres, Redis, Mailgun)
- Git-based deploy tres simple

**Inconvenients :**
- **Plus de free tier** depuis 2022 — minimum 5 USD/mois
- Couteux en production (Heroku Postgres = ~9 USD/mois minimum)
- Pas d'EU data center — souverainete impossible
- Depreciation progressive de l'offre EC2 (migration vers Salesforce)

#### Scaleway

**Avantages :**
- **Data center a Paris** — souverainete des donnees, conformite RGPD
- **100 EUR de credits gratuits** les 3 premiers mois — largement suffisant pour le PFA
- PostgreSQL Managed performant et configurable
- Containers Kubernetes disponibles si besoin futur
- Couts previsibles, facturation a la seconde

**Inconvenients :**
- Deploiement Docker moins automatique que Railway — necessite plus de config
- Moins de documentation pour les cas d'usage Docker Compose
- Dashboard moins polish que Railway/Heroku
- Support communautaire plus petit

### Estimation de cout mensuel

| Service | Railway | Heroku | Scaleway |
|---------|---------|--------|----------|
| Backend Django | 5 USD | 7 USD | 7.99 EUR |
| PostgreSQL | 5 USD | 9 USD | 9.99 EUR |
| Redis | 5 USD | 15 EUR | 9.99 EUR |
| **Total (3 services)** | **~15 USD** | **~31 USD** | **~27.97 EUR** |
| Free tier applicable ? | 5 USD credits | Non | 100 EUR credits (3 mois) |

### Recommandation

**Choix : Scaleway**

**Justification :**
1. **Souverainete des donnees** : Le projet est academique francais, les donnees utilisateur (emails, fichiers CSV) doivent rester en France. Scaleway est le seul avec un data center a Paris.
2. **Credits gratuits** : 100 EUR de credits pendant 3 mois couvrent largement la phase de developpement et de demonstration du PFA.
3. **Conformite RGPD** : Le cahier des charges exige la conformite RGPD. Heberger en France simplifie enormement cette exigence.
4. **Stack complete** : PostgreSQL Managed + Redis + containers Docker — tout est disponible nativement.
5. **Cout reel** : Apres les credits, ~28 EUR/mois est competitive avec Railway (~15 USD) et bien moins que Heroku (~31 USD).

**Plan B** : Railway — si la simplicite de deploiement devient critique pendant le sprint, Railway est le plus simple a mettre en place. On peut migrer vers Scaleway pour la production finale.

**Deploiement Docker Compose sur Scaleway :**
```bash
# Installer la CLI Scaleway
scw container cluster create name=dashbail-cluster

# Ou utiliser un VM DEV1-M avec Docker Compose
scw instance server create type=DEV1-M image=docker
ssh root@<IP> "docker-compose up -d"
```

---

## Synthese des decisions

| Domaine | Choix | Alternative |
|---------|-------|-------------|
| **LLM** | OpenAI GPT-4o | Mistral (plan B souverainete) |
| **Graphiques React** | Recharts | Chart.js (si besoin Canvas) |
| **Hebergement** | Scaleway (Paris) | Railway (si simplicite prioritaires) |

### Justification globale

Ces trois choix privilegient :
1. **La fiabilite** : GPT-4o (mode JSON natif), Recharts (React natif), Scaleway (Postgres managed)
2. **La productivite** : OpenAI (doc massive), Recharts (JSX declaratif), Railway/Scaleway (Docker natif)
3. **La conformite** : Scaleway (RGPD, data center FR), OpenAI (pas de stockage de donnees apres traitement)
4. **Le cout** : Budget estime ~90 USD/mois LLM + ~28 EUR/mois hebergement = ~120 EUR/mois total
