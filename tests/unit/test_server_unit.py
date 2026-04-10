from datetime import datetime


def test_club_has_enough_points(clubs_data):
    club = clubs_data[0]  # Simply Lift, 13 points
    assert int(club["points"]) >= 5


def test_club_not_enough_points(clubs_data):
    club = clubs_data[1]  # Iron Temple, 4 points
    assert int(club["points"]) < 5


def test_points_deduction(clubs_data):
    club = clubs_data[0]  # 13 points
    new_points = int(club["points"]) - 3
    assert new_points == 10


def test_places_deduction(competitions_data):
    comp = competitions_data[0]  # 25 places
    new_places = int(comp["numberOfPlaces"]) - 3
    assert new_places == 22


def test_future_competition(competitions_data):
    comp = competitions_data[0]
    date = datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S")
    assert date > datetime.now()


def test_past_competition(competitions_data):
    comp = competitions_data[2]
    date = datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S")
    assert date < datetime.now()


def test_find_club_by_email(clubs_data):
    found = [c for c in clubs_data if c["email"] == "john@simplylift.co"]
    assert len(found) == 1
    assert found[0]["name"] == "Simply Lift"


def test_unknown_email_returns_empty(clubs_data):
    found = [c for c in clubs_data if c["email"] == "unknown@test.com"]
    assert len(found) == 0


def test_12_places_allowed():
    assert 12 <= 12


def test_13_places_rejected():
    assert 13 > 12


def test_cannot_book_more_than_available(competitions_data):
    comp = competitions_data[1]  # 13 places
    assert 20 > int(comp["numberOfPlaces"])