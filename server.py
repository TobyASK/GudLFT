import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    # Charge la liste des clubs depuis le fichier JSON
    with open('clubs.json') as clubs_file:
        clubs = json.load(clubs_file)['clubs']
        return clubs


def load_competitions():
    # Charge la liste des compétitions depuis le fichier JSON
    with open('competitions.json') as competitions_file:
        competitions = json.load(competitions_file)['competitions']
        return competitions


def save_clubs():
    # Sauvegarde l'état actuel des clubs dans le fichier JSON
    with open('clubs.json', 'w') as clubs_file:
        json.dump({'clubs': clubs}, clubs_file)


def save_competitions():
    # Sauvegarde l'état actuel des compétitions dans le fichier JSON
    with open('competitions.json', 'w') as competitions_file:
        json.dump({'competitions': competitions}, competitions_file)


app = Flask(__name__)
app.secret_key = 'something_special'

# Chargement des données au démarrage de l'application
competitions = load_competitions()
clubs = load_clubs()


def find_club_by_email(clubs_list, email):
    # Retourne le club correspondant à l'email, ou None si inconnu
    matches = [c for c in clubs_list if c['email'] == email]
    return matches[0] if matches else None


def is_future_competition(competition):
    # Retourne True si la compétition n'est pas encore passée
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    return competition_date > datetime.now()


def get_booking_error(places_requested, club_points, available_places):
    # Vérifie les règles métier d'une réservation — retourne un message d'erreur ou None si valide
    if places_requested > 12:
        return 'Cannot book more than 12 places'
    if places_requested > available_places:
        return 'Not enough places available'
    if places_requested > club_points:
        return 'Not enough points'
    return None


@app.route('/')
def index():
    # Page d'accueil — formulaire de connexion
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    # Connexion par email — affiche le tableau de bord si l'email est reconnu
    club = find_club_by_email(clubs, request.form['email'])
    if not club:
        flash('Email not found')
        return render_template('index.html'), 404
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name, club_name):
    # Page de réservation — vérifie que la compétition n'est pas passée avant d'afficher le formulaire
    club = [c for c in clubs if c['name'] == club_name][0]
    competition = [c for c in competitions if c['name'] == competition_name][0]
    if club and competition:
        if not is_future_competition(competition):
            flash('Cannot book a past competition')
            return render_template('welcome.html', club=club, competitions=competitions), 400
        return render_template('booking.html', club=club, competition=competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club_name, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    # Traitement de la réservation — applique toutes les règles métier avant de valider
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_requested = int(request.form['places'])
    club_points = int(club['points'])
    available_places = int(competition['numberOfPlaces'])

    error = get_booking_error(places_requested, club_points, available_places)
    if error:
        flash(error)
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Déduction des places et des points après réservation validée
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_requested
    club['points'] = int(club['points']) - places_requested
    save_clubs()
    save_competitions()
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsBoard')
def points_board():
    # Tableau public des points — accessible sans connexion
    return render_template('points_board.html', clubs=clubs)


@app.route('/logout')
def logout():
    # Déconnexion — redirige vers la page d'accueil
    return redirect(url_for('index'))
