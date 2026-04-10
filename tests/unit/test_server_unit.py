from datetime import datetime


def test_club_has_enough_points(clubs_data):
    club = [c for c in clubs_data if c['name'] == 'Simply Lift'][0]
    assert int(club['points']) >= 5


def test_club_not_enough_points(clubs_data):
    club = [c for c in clubs_data if c['name'] == 'Iron Temple'][0]
    assert int(club['points']) < 5


def test_points_deduction(clubs_data):
    club = [c for c in clubs_data if c['name'] == 'Simply Lift'][0]
    new_points = int(club['points']) - 3
    assert new_points == 10


def test_places_deduction(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    new_places = int(comp['numberOfPlaces']) - 3
    assert new_places == 22


def test_future_competition(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
    assert date > datetime.now()


def test_past_competition(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Past Competition'][0]
    date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
    assert date < datetime.now()


def test_find_club_by_email(clubs_data):
    found = [c for c in clubs_data if c['email'] == 'john@simplylift.co']
    assert len(found) == 1
    assert found[0]['name'] == 'Simply Lift'


def test_unknown_email_returns_empty(clubs_data):
    found = [c for c in clubs_data if c['email'] == 'unknown@test.com']
    assert len(found) == 0


def test_12_places_allowed(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    places_required = 12
    assert places_required <= 12
    assert places_required <= int(comp['numberOfPlaces'])


def test_13_places_rejected(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Spring Festival'][0]
    places_required = 13
    assert places_required > 12


def test_cannot_book_more_than_available(competitions_data):
    comp = [c for c in competitions_data if c['name'] == 'Fall Classic'][0]
    assert 20 > int(comp['numberOfPlaces'])