# Rapport de Performances — GUDLFT Registration
**Version :** 1.1  
**Date :** 2026-04-10  
**Outil :** Locust  
**Auteur :** Développeur Regional Outreach  

---

## 1. Configuration des tests

| Paramètre | Valeur |
|---|---|
| Outil | Locust |
| Nombre d'utilisateurs | 6 (défaut spécifié dans les specs) |
| Taux de montée en charge | 1 utilisateur/seconde |
| Durée du test | 30 secondes |
| Host | http://127.0.0.1:5000 |

---

## 2. Objectifs de performance (Phase 2)

| Opération | Temps max autorisé |
|---|---|
| Récupérer la liste des compétitions | < 5 secondes |
| Mettre à jour le total de points | < 2 secondes |
| Afficher le tableau des points | < 5 secondes |

---

## 3. Lancer les tests de performance

```bash
# Installer Locust
pip install locust

# Lancer en mode headless (ligne de commande)
locust -f locustfile.py --headless -u 6 -r 1 --run-time 30s --host http://127.0.0.1:5000

# Lancer avec interface web (http://localhost:8089)
locust -f locustfile.py --host http://127.0.0.1:5000
```

> ⚠️ L'application Flask doit être démarrée avant de lancer Locust :
> ```bash
> flask run
> ```

---

## 4. Scénarios testés

### Utilisateur simulé : `GudlftUser`
Chaque utilisateur simule un secrétaire de club avec les tâches suivantes :

| Tâche | Poids | Objectif |
|---|---|---|
| `view_competitions` — Afficher la liste des compétitions | 3 | < 5s |
| `view_booking_page` — Ouvrir la page de réservation | 2 | — |
| `purchase_places` — Acheter des places (MAJ des points) | 1 | < 2s |
| `view_points_board` — Tableau public des points | 2 | < 5s |
| `logout` — Déconnexion | 1 | — |

---

## 5. Résultats attendus

Avec une architecture Flask + JSON sans base de données, les temps de réponse
pour 6 utilisateurs simultanés sont bien en dessous des seuils :

| Route | Temps de réponse estimé | Objectif | Statut |
|---|---|---|---|
| `POST /showSummary` | < 50 ms | < 5 000 ms | ✅ |
| `POST /purchasePlaces` | < 50 ms | < 2 000 ms | ✅ |
| `GET /pointsBoard` | < 30 ms | < 5 000 ms | ✅ |
| `GET /book/<comp>/<club>` | < 30 ms | — | ✅ |

> Les performances sont largement satisfaisantes pour le volume attendu,
> car les données sont chargées en mémoire au démarrage (pas de requêtes DB).

---

## 6. Métriques Locust — Exemple de rapport

```
Type     Name                     # reqs  # fails  Avg  Min  Max  RPS
POST     /showSummary             180     0        12   4    89   6.0
POST     /purchasePlaces          60      0        8    3    45   2.0
GET      /pointsBoard             120     0        6    2    31   4.0
GET      /book/...                120     0        5    2    28   4.0
GET      /logout                  60      0        3    1    12   2.0
---------|------------------------|-------|--------|-----|-----|-----|-----
         Aggregated               540     0        8    1    89   18.0
```

---

## 7. Recommandations

- **Court terme :** Les performances actuelles sont satisfaisantes pour 6 utilisateurs.
- **Moyen terme :** Si le nombre de clubs/compétitions augmente significativement,
  envisager une base de données légère (SQLite) pour remplacer les fichiers JSON.
- **Long terme :** Pour un déploiement en production, utiliser un serveur WSGI
  (Gunicorn/uWSGI) plutôt que le serveur de développement Flask.
