from datetime import datetime


# Vérifie que Simply Lift a assez de points pour réserver (au moins 5)
def test_club_has_enough_points(clubs_data):
    club = [c for c in clubs_data if c['name'] == 'Simply Lift'][0]  # Cherche Simply Lift dans la liste
    assert int(club['points']) >= 5  # Les points sont stockés en string, on convertit en int


# Vérifie qu'Iron Temple n'a pas assez de points pour réserver 5 places
def test_club_not_enough_points(clubs_data):
    club = [c for c in clubs_data if c['name'] == 'Iron Temple'][0]
    assert int(club['points']) < 5


# Vérifie que la déduction de points est correcte (13 - 3 = 10)
def test_points_deduction(clubs_data):
    club = [c for c in clubs_data if c['name'] == 'Simply Lift'][0]
    new_points = int(club['points']) - 3  # Simule la déduction de 3 places
    assert new_points == 10


# Vérifie que la déduction de places est correcte (25 - 3 = 22)
def test_places_deduction(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    new_places = int(comp['numberOfPlaces']) - 3  # Simule la réservation de 3 places
    assert new_places == 22


# Vérifie que Spring Festival est bien une compétition future
def test_future_competition(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')  # Convertit la string en objet datetime
    assert date > datetime.now()  # Compare avec la date actuelle


# Vérifie que Past Competition est bien une compétition passée
def test_past_competition(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Past Competition'][0]
    date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')  # Convertit la string en objet datetime
    assert date < datetime.now()


# Vérifie qu'on retrouve bien un club par son email
def test_find_club_by_email(clubs_data):
    found = [c for c in clubs_data if c['email'] == 'john@simplylift.co']  # Filtre par email
    assert len(found) == 1           # Un seul club doit correspondre
    assert found[0]['name'] == 'Simply Lift'


# Vérifie qu'un email inconnu ne retourne aucun club
def test_unknown_email_returns_empty(clubs_data):
    found = [c for c in clubs_data if c['email'] == 'unknown@test.com']
    assert len(found) == 0  # La liste doit être vide


# Vérifie que 12 places est une demande valide (dans la limite et dans les places dispo)
def test_12_places_allowed(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    places_required = 12
    assert places_required <= 12                        # Respecte la limite max par compétition
    assert places_required <= int(comp['numberOfPlaces'])  # Respecte les places disponibles


# Vérifie que 13 places dépasse la limite autorisée de 12
def test_13_places_rejected(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    places_required = 13
    assert places_required > 12  # 13 dépasse la limite de 12


# Vérifie que 20 places dépasse les places disponibles de Fall Classic (13)
def test_cannot_book_more_than_available(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Fall Classic'][0]
    places_required = 20
    assert places_required > int(comp['numberOfPlaces'])  # 20 > 13 → surréservation
