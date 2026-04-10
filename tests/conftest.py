import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import server


# Données de test pour les clubs : 3 clubs avec des soldes de points différents
# Simply Lift (13 pts) et She Lifts (12 pts) ont assez de points, Iron Temple (4 pts) non
@pytest.fixture
def clubs_data():
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    ]


# Données de test pour les compétitions :
# - Spring Festival : compétition future avec beaucoup de places (25)
# - Fall Classic : compétition future avec peu de places (13)
# - Past Competition : compétition passée, ne doit pas être réservable
@pytest.fixture
def competitions_data():
    return [
        {"name": "Spring Festival", "date": "2026-06-15 10:00:00", "numberOfPlaces": "25"},
        {"name": "Fall Classic", "date": "2026-10-22 13:30:00", "numberOfPlaces": "13"},
        {"name": "Past Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": "10"}
    ]


# Client Flask de test : écrit les données dans un dossier temporaire,
# recharge le module server pour repartir d'un état propre à chaque test
@pytest.fixture
def client(clubs_data, competitions_data, tmp_path):
    (tmp_path / "clubs.json").write_text(json.dumps({"clubs": clubs_data}))
    (tmp_path / "competitions.json").write_text(json.dumps({"competitions": competitions_data}))
    os.chdir(tmp_path)

    import importlib
    importlib.reload(server)

    server.app.config["TESTING"] = True
    with server.app.test_client() as c:
        yield c
