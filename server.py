"""
GUDLFT Registration - Application de réservation régionale
Version: 1.1

UTILISATION:
1. Installer les dépendances: pip install -r requirements.txt
2. Lancer l'app: flask run (ou python -m flask run)
3. Accéder à: http://127.0.0.1:5000

ROUTES PRINCIPALES:
- / (GET)                  : Page d'accueil
- /showSummary (POST)      : Connexion avec email
- /book/<comp>/<club> (GET): Page de réservation
- /purchasePlaces (POST)   : Achat de places (déduction points)
- /pointsBoard (GET)       : Tableau public des points (sans connexion)
- /logout (GET)            : Déconnexion

DONNÉES:
- clubs.json              : Liste des clubs et points
- competitions.json       : Liste des compétitions

SPÉCIFICATIONS:
- Phase 1: Authentification + réservation (max 12 places)
- Phase 2: Tableau public des points
- Persistance: saveClubs() et saveCompetitions() sauvegardent les données
"""

import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def saveClubs():
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=2)


def saveCompetitions():
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=2)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # BUG FIX #1 : email inconnu faisait crasher l'app (IndexError)
    email = request.form.get('email', '').strip()
    found = [club for club in clubs if club['email'] == email]
    if not found:
        flash("Sorry, that email wasn't found.")
        return render_template('index.html'), 404
    club = found[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)

    if not foundClub or not foundCompetition:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', club=foundClub or {}, competitions=competitions), 404

    # BUG FIX #5 : interdire la reservation sur une competition passee
    comp_date = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    if comp_date <= datetime.now():
        flash("This competition is already over, bookings are closed.")
        return render_template('welcome.html', club=foundClub, competitions=competitions), 400

    return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', club=club or {}, competitions=competitions), 404

    try:
        placesRequired = int(request.form['places'])
    except (ValueError, TypeError):
        flash("Invalid number of places.")
        return render_template('booking.html', club=club, competition=competition), 400

    availablePlaces = int(competition['numberOfPlaces'])
    clubPoints = int(club['points'])

    # BUG FIX #4 : maximum 12 places par competition
    if placesRequired <= 0:
        flash("Number of places must be greater than 0.")
        return render_template('booking.html', club=club, competition=competition), 400

    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return render_template('booking.html', club=club, competition=competition), 400

    # BUG FIX #282 : pas plus de places que disponibles
    if availablePlaces <= 0:
        flash("This competition is fully booked.")
        return render_template('booking.html', club=club, competition=competition), 400

    if placesRequired > availablePlaces:
        flash("Not enough places available. Only {} left.".format(availablePlaces))
        return render_template('booking.html', club=club, competition=competition), 400

    # BUG FIX #2 : pas plus de points que disponibles
    if placesRequired > clubPoints:
        flash("Not enough points. Your club has {} points.".format(clubPoints))
        return render_template('booking.html', club=club, competition=competition), 400

    # BUG FIX #6 : deduire les points ET les places
    competition['numberOfPlaces'] = availablePlaces - placesRequired
    club['points'] = clubPoints - placesRequired

    # Sauvegarde dans les fichiers JSON
    saveClubs()
    saveCompetitions()

    flash('Great - booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# PHASE 2 / Issue #7 : tableau public des points, sans connexion requise
@app.route('/pointsBoard')
def pointsBoard():
    return render_template('points_board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))