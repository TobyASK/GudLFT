# GudLFT — Présentation du projet

## Contexte

Application de réservation de compétitions sportives locales.  
Les secrétaires de clubs réservent des places pour leurs athlètes via un système de points.

Lancer l'application :
```bash
pip install -r requirements.txt
flask --app server run
```

---

## Problème de départ

Le projet existait mais contenait **6 bugs** et **1 fonctionnalité manquante**.  
Les tests étaient déjà écrits et échouaient — l'objectif était de corriger le code pour les faire passer.

---

## Bugs corrigés

| # | Bug | Symptôme | Correction |
|---|-----|----------|------------|
| 1 | Email inconnu | `IndexError` → crash | Vérification de la liste, retour 404 |
| 2 | Points insuffisants | Réservation acceptée quand même | Vérification `placesRequired > clubPoints` |
| 4 | Limite 12 places | On pouvait en réserver 50 | Vérification `placesRequired > 12` |
| 5 | Compétition passée | On pouvait réserver en 2020 | Vérification de la date avec `datetime.now()` |
| 6 | Points non déduits | Le solde ne bougeait pas | Ajout de `saveClubs()` / `saveCompetitions()` |
| 282 | Surréservation | On pouvait vider une compétition | Vérification `placesRequired >= availablePlaces - 1` |

---

## Fonctionnalité ajoutée

**Tableau public des points** (`/pointsBoard`)  
- Accessible sans connexion  
- Liste tous les clubs et leur solde de points  
- Répond à une demande de transparence des organisations

---

## Architecture

```
server.py          → 6 routes Flask, logique métier linéaire
clubs.json         → données des clubs (nom, email, points)
competitions.json  → données des compétitions (nom, date, places)
templates/         → HTML Jinja2
tests/
  unit/            → 11 tests (logique pure)
  integration/     → 3 tests (interaction entre composants)
  functional/      → 12 tests (comportement HTTP)
```

---

## Résultats des tests

Lancer les tests :
```bash
python -m pytest tests/ -v
```

Lancer avec la couverture :
```bash
python -m pytest tests/ --cov=server --cov-report=term-missing
```

Résultat :
```
26/26 tests passent
Couverture : 92%  (objectif spec : 60%)
```

---

## Workflow Git

```
master (stable)
  └── QA (branche de validation)
        ├── bug/unknown-email-crashes-app
        ├── bug/points-not-deducted
        ├── bug/club-points-exceed-allowed
        ├── bug/max-12-places-per-competition
        ├── bug/booking-past-competitions
        ├── bug/exceed-available-places
        └── feature/points-display-board
```

Créer une branche depuis QA :
```bash
git checkout -b bug/nom-du-bug QA
```

Merger dans QA après correction :
```bash
git checkout QA
git merge --no-ff bug/nom-du-bug
```

Voir toutes les branches :
```bash
git branch -a
```

Chaque branche = un bug ou une feature.  
QA n'est pas mergée dans master — elle attend validation.

---

## Respect des spécifications

| Critère | Statut |
|---------|--------|
| Connexion par email | ✅ |
| Réservation avec points | ✅ |
| Limite 12 places par compétition | ✅ |
| Pas de surréservation | ✅ |
| Compétitions passées non réservables | ✅ |
| Tableau public des points | ✅ |
| Couverture > 60% | ✅ 92% |
| Tests organisés par type | ✅ |
| Une branche par bug/feature | ✅ |
| QA séparée de master | ✅ |
