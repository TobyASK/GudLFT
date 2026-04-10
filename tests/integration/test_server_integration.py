from unittest.mock import patch
import server


def test_purchase_deducts_points(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    assert int(club['points']) == 10


def test_purchase_deducts_places(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    comp = [c for c in server.competitions if c['name'] == 'Spring Festival'][0]
    assert int(comp['numberOfPlaces']) == 22


def test_points_not_deducted_on_failed_booking(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '5'
        })
    club = [c for c in server.clubs if c['name'] == 'Iron Temple'][0]
    assert int(club['points']) == 4