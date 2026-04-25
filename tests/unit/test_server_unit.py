import server


def test_find_club_by_email(clubs_data):
    # Vérifie que find_club_by_email retourne le bon club pour un email valide
    club = server.find_club_by_email(clubs_data, 'john@simplylift.co')
    assert club is not None
    assert club['name'] == 'Simply Lift'


def test_unknown_email_returns_none(clubs_data):
    # Vérifie que find_club_by_email retourne None pour un email inconnu
    club = server.find_club_by_email(clubs_data, 'unknown@test.com')
    assert club is None


def test_future_competition(competitions_data):
    # Vérifie que is_future_competition retourne True pour Spring Festival (futur)
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    assert server.is_future_competition(comp) is True


def test_past_competition(competitions_data):
    # Vérifie que is_future_competition retourne False pour Past Competition (passé)
    comp = [c for c in competitions_data if c['name'] == 'Past Competition'][0]
    assert server.is_future_competition(comp) is False


def test_booking_valid_returns_no_error():
    # Vérifie que 3 places avec assez de points et de places dispo ne produit aucune erreur
    assert server.get_booking_error(places_requested=3, club_points=13, available_places=25) is None


def test_booking_too_many_places_returns_error():
    # Vérifie que get_booking_error refuse plus de 12 places (règle limite par compétition)
    error = server.get_booking_error(places_requested=13, club_points=50, available_places=25)
    assert error == 'Cannot book more than 12 places'


def test_booking_exceeds_available_returns_error():
    # Vérifie que get_booking_error refuse si les places demandées dépassent les places disponibles
    error = server.get_booking_error(places_requested=12, club_points=50, available_places=5)
    assert error == 'Not enough places available'


def test_booking_not_enough_points_returns_error():
    # Vérifie que get_booking_error refuse si le club n'a pas assez de points
    error = server.get_booking_error(places_requested=5, club_points=4, available_places=25)
    assert error == 'Not enough points'


def test_booking_exactly_12_places_allowed():
    # Vérifie que 12 places exactement est accepté (limite incluse)
    assert server.get_booking_error(places_requested=12, club_points=13, available_places=25) is None


def test_booking_exactly_available_places_allowed():
    # Vérifie que réserver exactement toutes les places disponibles est accepté
    assert server.get_booking_error(places_requested=10, club_points=13, available_places=10) is None
