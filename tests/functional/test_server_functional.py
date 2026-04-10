from unittest.mock import patch


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Simply Lift' in response.data


def test_login_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@test.com'})
    assert response.status_code != 500


def test_book_page(client):
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Spring Festival' in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_points_board(client):
    response = client.get('/pointsBoard')
    assert response.status_code == 200


def test_points_board_shows_clubs(client):
    response = client.get('/pointsBoard')
    assert b'Simply Lift' in response.data
    assert b'Iron Temple' in response.data


def test_purchase_valid(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    assert response.status_code == 200