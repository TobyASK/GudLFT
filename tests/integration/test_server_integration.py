from unittest.mock import patch
import server


# Cas d'usage complet : un club se connecte, réserve des places, et son solde est mis à jour
# Simply Lift (13 pts) se connecte, réserve 3 places pour Spring Festival
# → la page de confirmation s'affiche ET les points sont bien déduits en mémoire
def test_full_booking_workflow(client):
    # Étape 1 : connexion par email
    login_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert login_response.status_code == 200

    # Étape 2 : réservation de 3 places
    with patch('server.save_clubs'), patch('server.save_competitions'):
        booking_response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': '3'
        })
    assert booking_response.status_code == 200
    assert b'Great-booking complete!' in booking_response.data

    # Étape 3 : vérification que les points et les places ont bien été déduits en mémoire
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    comp = [c for c in server.competitions if c['name'] == 'Spring Festival'][0]
    assert int(club['points']) == 10       # 13 - 3 = 10
    assert int(comp['numberOfPlaces']) == 22  # 25 - 3 = 22
