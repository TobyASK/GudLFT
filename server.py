import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


# Charge la liste des clubs depuis le fichier JSON
def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


# Charge la liste des compétitions depuis le fichier JSON
def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


# Sauvegarde l'état actuel des clubs dans le fichier JSON
def saveClubs():
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c)


# Sauvegarde l'état actuel des compétitions dans le fichier JSON
def saveCompetitions():
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps)


app = Flask(__name__)
app.secret_key = 'something_special'

# Chargement des données au démarrage de l'application
competitions = loadCompetitions()
clubs = loadClubs()

# Page d'accueil — formulaire de connexion
@app.route('/')
def index():
    return render_template('index.html')


# Connexion par email — affiche le tableau de bord si l'email est reconnu
@app.route('/showSummary',methods=['POST'])
def showSummary():
    found = [club for club in clubs if club['email'] == request.form['email']]
    if not found:
        flash('Email not found')
        return render_template('index.html'), 404
    club = found[0]
    return render_template('welcome.html',club=club,competitions=competitions)


# Page de réservation — vérifie que la compétition n'est pas passée avant d'afficher le formulaire
@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        competitionDate = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
        # Interdit la réservation sur une compétition dont la date est dépassée
        if competitionDate < datetime.now():
            flash('Cannot book a past competition')
            return render_template('welcome.html', club=foundClub, competitions=competitions), 400
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


# Traitement de la réservation — applique toutes les règles métier avant de valider
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    clubPoints = int(club['points'])
    availablePlaces = int(competition['numberOfPlaces'])

    # Règle 1 : un club ne peut pas réserver plus de 12 places par compétition
    if placesRequired > 12:
        flash('Cannot book more than 12 places')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Règle 2 : on ne peut pas réserver plus de places qu'il n'en reste disponibles
    if placesRequired >= availablePlaces - 1:
        flash('Not enough places available')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Règle 3 : le club doit avoir suffisamment de points (1 point = 1 place)
    if placesRequired > clubPoints:
        flash('Not enough points')
        return render_template('welcome.html', club=club, competitions=competitions), 400

    # Déduction des places et des points après réservation validée
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    saveClubs()
    saveCompetitions()
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# Tableau public des points — accessible sans connexion
@app.route('/pointsBoard')
def pointsBoard():
    return render_template('points_board.html', clubs=clubs)


# Déconnexion — redirige vers la page d'accueil
@app.route('/logout')
def logout():
    return redirect(url_for('index'))
