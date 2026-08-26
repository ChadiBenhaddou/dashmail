# Présentation — Dashboard X

## Slide 1 — Page de titre
Dashboard X — Génération automatique de rapports visuels par email
PFA 2024-2025
Équipe: Chadi, Ayoub, Haitem, Moussa

## Slide 2 — Problématique
- Les utilisateurs non techniques passent des heures à créer des rapports Excel/PowerPoint
- Les outils BI (Power BI, Tableau) sont complexes et coûteux
- Besoin: transformer un simple email avec fichier en rapport visuel complet

## Slide 3 — Solution proposée
- Flux simple: email + fichier → analyse IA → dashboard interactif
- Aucune inscription requise — accès par lien unique
- Technologies: Django, React, OpenAI, Docker

## Slide 4 — Architecture technique
```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Email      │────▶│   Django     │────▶│   Celery     │
│  (Gmail,     │     │   API REST   │     │   + Redis    │
│   Outlook)   │     │              │     │              │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                           ┌─────────────────────┼─────────────────────┐
                           │                     │                     │
                    ┌──────▼──────┐      ┌───────▼──────┐     ┌───────▼──────┐
                    │  PostgreSQL  │      │  OpenAI API  │     │  Frontend    │
                    │  (données)   │      │  (analyse)   │     │  React       │
                    └─────────────┘      └──────────────┘     │  + Recharts  │
                                                              └──────────────┘
```
- Backend Django (API REST)
- Celery + Redis (tâches asynchrones)
- PostgreSQL (données)
- Frontend React + Recharts (visualisation)
- LLM OpenAI (analyse intelligente)

## Slide 5 — Flux utilisateur
1. Envoi email avec CSV/Excel
2. Parsing automatique (pandas)
3. Analyse IA → choix des graphiques
4. Génération du dashboard
5. Email avec lien vers le dashboard
6. Consultation sans connexion

## Slide 6 — Démonstration
- Capture d'écran du dashboard complet
- Les 4 états: succès, chargement, erreur, mobile

## Slide 7 — Stack technique
| Composant | Technologie | Justification |
|-----------|------------|---------------|
| Backend | Django 5 + DRF | Robuste, écosystème riche |
| Async | Celery + Redis | Fiabilité, retry |
| DB | PostgreSQL | Production-ready |
| Frontend | React + Vite | Performance, DX |
| Charts | Recharts | Intégration React native |
| LLM | OpenAI GPT-4o | JSON mode, qualité |
| Infra | Docker Compose | Reproductibilité |

## Slide 8 — Défis et solutions
| Défi | Solution |
|------|----------|
| Fichiers CSV hétérogènes | Détection auto des types + nettoyage pandas |
| Hallucination LLM sur les chiffres | Pandas est la source de vérité, LLM ne génère que texte |
| Timeout de l'API LLM | Retry + fallback sur heuristiques |
| Fichiers corrompus | Gestion d'erreurs spécifique + email d'explication |
| Sans inscription | UUID non devinable + lien temporaire |

## Slide 9 — Améliorations futures
- PDF téléchargeable
- Upload manuel depuis le dashboard
- Rapports récurrents programmés
- Connecteurs SQL/ERP/CRM
- Multilingue
- Facturation SaaS

## Slide 10 — Merci / Questions
Dashboard X — Merci de votre attention
