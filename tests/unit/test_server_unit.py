import server


# Vérifie que find_club_by_email retourne le bon club pour un email valide
def test_find_club_by_email(clubs_data):
    club = server.find_club_by_email(clubs_data, 'john@simplylift.co')
    assert club is not None
    assert club['name'] == 'Simply Lift'


# Vérifie que find_club_by_email retourne None pour un email inconnu
def test_unknown_email_returns_none(clubs_data):
    club = server.find_club_by_email(clubs_data, 'unknown@test.com')
    assert club is None


# Vérifie que is_future_competition retourne True pour Spring Festival (futur)
def test_future_competition(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    assert server.is_future_competition(comp) is True


# Vérifie que is_future_competition retourne False pour Past Competition (passé)
def test_past_competition(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Past Competition'][0]
    assert server.is_future_competition(comp) is False


# Vérifie que 3 places avec assez de points et de places dispo ne produit aucune erreur
def test_booking_valid_returns_no_error():
    assert server.get_booking_error(places_requested=3, club_points=13, available_places=25) is None


# Vérifie que get_booking_error refuse plus de 12 places (règle limite par compétition)
def test_booking_too_many_places_returns_error():
    error = server.get_booking_error(places_requested=13, club_points=50, available_places=25)
    assert error == 'Cannot book more than 12 places'


# Vérifie que get_booking_error refuse si les places demandées dépassent les places disponibles
def test_booking_exceeds_available_returns_error():
    error = server.get_booking_error(places_requested=12, club_points=50, available_places=5)
    assert error == 'Not enough places available'


# Vérifie que get_booking_error refuse si le club n'a pas assez de points
def test_booking_not_enough_points_returns_error():
    error = server.get_booking_error(places_requested=5, club_points=4, available_places=25)
    assert error == 'Not enough points'


# Vérifie que 12 places exactement est accepté (limite incluse)
def test_booking_exactly_12_places_allowed():
    assert server.get_booking_error(places_requested=12, club_points=13, available_places=25) is None


# Vérifie que réserver exactement toutes les places disponibles est accepté
def test_booking_exactly_available_places_allowed():
    assert server.get_booking_error(places_requested=10, club_points=13, available_places=10) is None
