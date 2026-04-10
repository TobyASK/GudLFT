# Rapport de Tests — GUDLFT Registration
**Version :** 1.1  
**Date :** 2026-04-10  
**Auteur :** Développeur Regional Outreach  

---

## 1. Environnement de test

| Élément | Valeur |
|---|---|
| Framework | pytest |
| Coverage | pytest-cov |
| Python | 3.x |
| Flask | 3.x |

---

## 2. Structure des tests

```
tests/
├── unit/
│   └── test_server_unit.py        (18 tests)
├── integration/
│   └── test_server_integration.py (27 tests)
└── functional/
    └── test_server_functional.py  (11 tests)
```

**Total : 56 tests** — ratio unitaires/autres ≈ 2:1 ✅

---

## 3. Lancer les tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=server --cov-report=html --cov-report=term

# Par catégorie
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/functional/ -v
```

---

## 4. Issues GitHub corrigées

### Issue #1 — Crash sur email inconnu (CRITIQUE)
- **Symptôme :** `IndexError: list index out of range` quand l'email n'existe pas
- **Cause :** `[club for club in clubs if club['email'] == email][0]` sans vérification
- **Correction :** Vérification de la liste + retour 404 avec message flash "Email introuvable"
- **Tests :** `test_login_invalid_email_returns_404`, `test_login_with_unknown_email`

### Issue #2 — Clubs ne peuvent pas dépenser plus de points qu'ils n'en ont
- **Symptôme :** Réservation confirmée même sans points suffisants
- **Cause :** Aucune vérification du solde de points dans `purchasePlaces`
- **Correction :** Condition `if placesRequired > clubPoints` + message d'erreur
- **Tests :** `test_purchase_not_enough_points`, `test_cannot_book_without_sufficient_points`

### Issue #4 — Limite de 12 places par compétition non appliquée
- **Symptôme :** Réservation de plus de 12 places confirmée
- **Cause :** Aucune limite dans `purchasePlaces`
- **Correction :** Condition `if placesRequired > 12` + message d'erreur
- **Tests :** `test_purchase_more_than_12_places`, `test_cannot_overbook_competition`

### Issue #5 — Réservation sur des compétitions passées
- **Symptôme :** Confirmation de réservation sur une compétition déjà terminée
- **Cause :** Aucun filtre de date dans `book()` et `showSummary()`
- **Correction :** Comparaison avec `datetime.now()` dans les deux routes
- **Tests :** `test_past_competitions_not_shown`, `test_cannot_book_past_competition`

### Issue #6 — Les points ne sont pas déduits après réservation
- **Symptôme :** Solde de points inchangé après achat de places
- **Cause :** La ligne de déduction était absente dans `purchasePlaces`
- **Correction :** `club['points'] = clubPoints - placesRequired`
- **Tests :** `test_purchase_deducts_points`

### Issue #282 — Réservation au-delà des places disponibles
- **Symptôme :** Confirmation même quand `placesRequired > numberOfPlaces`
- **Cause :** Aucune vérification du stock de places avant déduction
- **Correction :** Condition `if placesRequired > availablePlaces` + message d'erreur
- **Tests :** `test_purchase_more_than_available`, `test_cannot_book_full_competition`

---

## 5. Fonctionnalité Phase 2 ajoutée

### Issue #7 — Tableau public des points (`/pointsBoard`)
- Accessible sans connexion
- Affiche le nom et les points de chaque club
- Template : `templates/points_board.html`
- **Tests :** `test_points_board_accessible_without_login`, `test_points_board_shows_all_clubs`, `test_points_board_shows_points`

---

## 6. Couverture cible

| Fichier | Couverture cible |
|---|---|
| server.py | ≥ 60% |

```bash
# Générer le rapport HTML de couverture
pytest tests/ --cov=server --cov-report=html
open htmlcov/index.html
```

---

## 7. Happy paths testés

| Scénario | Résultat attendu |
|---|---|
| Connexion avec email valide | 200, page welcome |
| Affichage des compétitions futures uniquement | Liste filtrée visible |
| Réservation valide (3 places, assez de points) | 200, confirmation |
| Points correctement déduits après réservation | Solde mis à jour |
| Places correctement déduites après réservation | Stock mis à jour |
| Tableau des points sans connexion | 200, tous les clubs visibles |
| Déconnexion | Redirection vers index |

---

## 8. Sad paths testés

| Scénario | Code retour | Message attendu |
|---|---|---|
| Email inconnu | 404 | "Email introuvable" |
| Réservation > 12 places | 400 | Message limite 12 |
| Pas assez de points | 400 | Message points insuffisants |
| Compétition complète (0 places) | 400 | "Compétition complète" |
| Réservation > places disponibles | 400 | Nombre de places restantes |
| Compétition passée (route /book) | 400 | "Compétition passée" |
| Valeur non numérique pour les places | 400 | "Nombre invalide" |
| Réservation de 0 place | 400 | "Doit être > 0" |
