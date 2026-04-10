from unittest.mock import patch


# Vérifie que la page d'accueil est accessible
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


# Vérifie qu'un email valide affiche bien le tableau de bord avec l'email du club
def test_login_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'john@simplylift.co' in response.data


# Vérifie qu'un email inconnu retourne une erreur 404
def test_login_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@test.com'})
    assert response.status_code == 404


# Vérifie que la page de réservation s'affiche correctement pour une compétition future
def test_book_page(client):
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Spring Festival' in response.data


# Vérifie qu'on ne peut pas accéder à la page de réservation d'une compétition passée
def test_book_past_competition(client):
    response = client.get('/book/Past Competition/Simply Lift')
    assert response.status_code == 400


# Vérifie que la déconnexion redirige bien vers l'accueil (302)
def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


# Vérifie que le tableau des points est accessible sans connexion
def test_points_board(client):
    response = client.get('/pointsBoard')
    assert response.status_code == 200


# Vérifie que le tableau des points affiche bien les noms des clubs
def test_points_board_shows_clubs(client):
    response = client.get('/pointsBoard')
    assert b'Simply Lift' in response.data
    assert b'Iron Temple' in response.data


# Vérifie qu'une réservation valide retourne 200
# Simply Lift (13 pts) réserve 3 places pour Spring Festival (25 places)
def test_purchase_valid(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    assert response.status_code == 200


# Vérifie qu'on ne peut pas réserver plus de 12 places (limite par compétition)
def test_purchase_too_many_places(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '13'
        })
    assert response.status_code == 400


# Vérifie qu'on ne peut pas réserver si le club n'a pas assez de points
# Iron Temple (4 pts) tente de réserver 5 places → refus
def test_purchase_not_enough_points(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '5'
        })
    assert response.status_code == 400


# Vérifie qu'on ne peut pas réserver plus de places qu'il n'en reste disponibles
# Fall Classic a 13 places, Simply Lift tente d'en réserver 12 → refus
def test_purchase_more_than_available(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Fall Classic',
            'places': '12'
        })
    assert response.status_code == 400
