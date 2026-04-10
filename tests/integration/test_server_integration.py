from unittest.mock import patch
import server


# Vérifie que les points du club sont bien déduits après une réservation réussie
# Simply Lift part de 13 points, réserve 3 places → doit avoir 10 points
def test_purchase_deducts_points(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    assert int(club['points']) == 10


# Vérifie que les places de la compétition sont bien déduites après une réservation réussie
# Spring Festival part de 25 places, 3 réservées → doit avoir 22 places
def test_purchase_deducts_places(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    comp = [c for c in server.competitions if c['name'] == 'Spring Festival'][0]
    assert int(comp['numberOfPlaces']) == 22


# Vérifie que les points ne sont PAS déduits si la réservation échoue
# Iron Temple (4 pts) tente de réserver 5 places → refus, solde doit rester à 4
def test_points_not_deducted_on_failed_booking(client):
    with patch('server.saveClubs'), patch('server.saveCompetitions'):
        client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '5'
        })
    club = [c for c in server.clubs if c['name'] == 'Iron Temple'][0]
    assert int(club['points']) == 4
