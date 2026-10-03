from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from passlib.context import CryptContext
from pytz import timezone

from .db import connect
from .main import db
from .models import (Album, ApparaitDans, Artiste, Contient, Cree, Ecoute,
                     Groupe, Morceau, ParticipeA, Playlist, Publie, Suit,
                     Utilisateur)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT 
                m."numMorc", m."titreMorceau", m."duree", m."paroles",
                r."Nb_Ecoutes_Uniques", r."Remuneration_Euro"
            FROM dataset.rapport_popularite_morceaux r
            JOIN dataset.morceau m ON r."ID_Morceau" = m."numMorc"
            ORDER BY r."Nb_Ecoutes_Uniques" DESC
            """)
            top_morceaux = cursor.fetchall()
    
    morceaux = [
        {
            'numMorc': row[0],
            'titreMorceau': row[1],
            'duree': row[2],
            'paroles': row[3],
            'Nb_Ecoutes_Uniques': row[4],
            'Remuneration_Euro': row[5]
        }
        for row in top_morceaux
    ]
    
    return render_template('home.html', morceaux=morceaux)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM dataset.utilisateur WHERE email = %s", (email,))
                user_data = cursor.fetchone()
                user = Utilisateur(pseudonyme=user_data[0], email=user_data[1],
                                   motDePasse=user_data[2], dateInscription=user_data[3],
                                   numUsr=user_data[4]) if user_data else None
        
        password_ctx = CryptContext(schemes=['bcrypt'])
                
        if user and password_ctx.verify(password, user.motDePasse):
            login_user(user)
            flash(f'Bravo {user.pseudonyme}, vous êtes bien connecté sur The Wave !', 'success')
        else:
            flash('Email ou mot de passe invalide', 'danger')
    
    return render_template('login.html')

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'success')
    return redirect(url_for('main.login'))

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search_type = 'morceaux'
    results = {
        'morceaux': [],
        'artistes': [],
        'albums': [],
        'playlists': []
    }
    
    keyword = ''
    search_type = 'morceaux'

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').lower()
        search_type = request.form.get('search_type')

        if search_type == 'morceaux':
            with connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    SELECT * FROM dataset.morceau
                    WHERE LOWER("titreMorceau") LIKE %s
                    """, (f'%{keyword}%',))
                    results['morceaux'] = [
                        Morceau(
                            numMorc=row[0],
                            titreMorceau=row[1],
                            duree=row[2],
                            paroles=row[3]
                        )
                        for row in cursor.fetchall()
                    ]

        elif search_type == 'artistes':
            with connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    SELECT * FROM dataset.artiste
                    WHERE LOWER("nom") LIKE %s OR LOWER("prenom") LIKE %s
                    """, (f'%{keyword}%', f'%{keyword}%'))
                    results['artistes'] = [
                        Artiste(
                            numArt=row[0],
                            nom=row[1],
                            prenom=row[2],
                            nationalite=row[3],
                            dateNaissance=row[4],
                            dateDeces=row[5]
                        )
                        for row in cursor.fetchall()
                    ]

        elif search_type == 'albums':
            with connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    SELECT * FROM dataset.album
                    WHERE LOWER("titreAlbum") LIKE %s
                    """, (f'%{keyword}%',))
                    results['albums'] = [
                        Album(
                            numAlb=row[0],
                            titreAlbum=row[1],
                            dateParution=row[2],
                            description=row[4]
                        )
                        for row in cursor.fetchall()
                    ]

        elif search_type == 'playlists':
            with connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    SELECT * FROM dataset.playlist
                    WHERE LOWER("titrePlaylist") LIKE %s
                    """, (f'%{keyword}%',))
                    results['playlists'] = [
                        Playlist(
                            numPlay=row[0],
                            titrePlaylist=row[1],
                            visibilite=row[2],
                            description=row[3]
                        )
                        for row in cursor.fetchall()
                    ]

    return render_template('search.html', results=results, search_type=search_type, keyword=keyword)

@main.route('/groupe/<int:numGrp>')
@login_required
def groupe_page(numGrp):

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.groupe WHERE "numGrp" = %s', (numGrp,))
            groupe_data = cursor.fetchone()
            if not groupe_data:
                flash("Groupe non trouvé", 'danger')
                return redirect(url_for('main.groupes'))
            groupe = Groupe(
                numGrp=groupe_data[0],
                nomGroupe=groupe_data[1],
                dateCreation=groupe_data[2],
                nationalite=groupe_data[3],
                gerneMusical=groupe_data[4]
            )
    
            cursor.execute("""
            SELECT a.nom, a.prenom, a.nationalite, a."dateNaissance", a."dateDeces", p.role
            FROM dataset.artiste a
            JOIN dataset.participe_a p ON a."numArt" = p."numArt"
            WHERE p."numGrp" = %s
            """, (numGrp,))
            membres = [
                {
                    'nom': row[0],
                    'prenom': row[1],
                    'nationalite': row[2],
                    'dateNaissance': row[3],
                    'dateDeces': row[4],
                    'role': row[5]
                }
                for row in cursor.fetchall()
            ]
    
            cursor.execute("""
            SELECT a."numAlb", a."titreAlbum", a."dateParution", a.description
            FROM dataset.album a
            JOIN dataset.publie p ON a."numAlb" = p."numAlb"
            WHERE p."numGrp" = %s
            """, (numGrp,))
            albums = [
                {
                    'numAlb': row[0],
                    'titreAlbum': row[1],
                    'dateParution': row[2],
                    'description': row[3]
                }
                for row in cursor.fetchall()
            ]
    
            cursor.execute("""
            SELECT COUNT(*)
            FROM dataset.utilisateur u
            JOIN dataset.suit s ON u."numUsr" = s."idSuiveur"
            WHERE
                s."idSuivi" = %s
                AND s."typeSuivi" = 'group_follow'
            """, (groupe.numGrp,))
            followers_count = cursor.fetchone()[0]

    return render_template('group.html', groupe=groupe, albums=albums, membres=membres, followers_count=followers_count)

@main.route('/groupes')
@login_required
def groupes():
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dataset.groupe")
            groupes_data = cursor.fetchall()
    
    all_groupes = [
        Groupe(
            numGrp=row[0],
            nomGroupe=row[1],
            dateCreation=row[2],
            nationalite=row[3],
            gerneMusical=row[4]
        )
        for row in groupes_data
    ]
    return render_template('group-catalog.html', groupes=all_groupes)

@main.route('/artiste/<int:artiste_id>')
@login_required
def artiste_page(artiste_id):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.artiste WHERE "numArt" = %s', (artiste_id,))
            artiste_data = cursor.fetchone()
            if not artiste_data:
                flash("Artiste non trouvé", 'danger')
                return redirect(url_for('main.artistes'))
    artiste = Artiste(
        numArt=artiste_data[0],
        nom=artiste_data[1],
        prenom=artiste_data[2],
        nationalite=artiste_data[3],
        dateNaissance=artiste_data[4],
        dateDeces=artiste_data[5]
    )
    
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT g."nomGroupe", p."role", p."dateEntree", p."dateSortie"
            FROM dataset.groupe g
            JOIN dataset.participe_a p ON g."numGrp" = p."numGrp"
            WHERE p."numArt" = %s
            """, (artiste.numArt,))
            groupes = [
                {
                    'nomGroupe': row[0],
                    'role': row[1],
                    'dateEntree': row[2],
                    'dateSortie': row[3]
                }
                for row in cursor.fetchall()
            ]
    
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT *
            FROM dataset.morceau m
            JOIN dataset.apparait_dans ad ON m."numMorc" = ad."numMorc"
            WHERE ad."numArt" = %s
            """, (artiste.numArt,))
            morceaux = [
                Morceau(
                    numMorc=row[0],
                    titreMorceau=row[1],
                    duree=row[2],
                    paroles=row[3]
                )
                for row in cursor.fetchall()
            ]
    return render_template('artist.html', artiste=artiste, groupes=groupes, morceaux=morceaux)

@main.route('/artistes')
@login_required
def artistes():
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dataset.artiste")
            artists_data = cursor.fetchall()
    
    artists = [
        Artiste(
            numArt=row[0],
            nom=row[1],
            prenom=row[2],
            nationalite=row[3],
            dateNaissance=row[4],
            dateDeces=row[5]
        )
        for row in artists_data
    ]
    return render_template('artist-catalog.html', artists=artists)

@main.route('/album/<int:album_id>')
@login_required
def album_page(album_id):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.album WHERE "numAlb" = %s', (album_id,))
            album_data = cursor.fetchone()
            if not album_data:
                flash("Album non trouvé", 'danger')
                return redirect(url_for('main.albums'))
    album = Album(
        numAlb=album_data[0],
        titreAlbum=album_data[1],
        dateParution=album_data[2],
        description=album_data[4]
    )
    
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT m."numMorc", m."titreMorceau", m."duree", m."paroles"
            FROM dataset.morceau m
            JOIN dataset.contient c ON m."numMorc" = c."numMorc"
            WHERE c."numAlb" = %s
            ORDER BY c."ordre"
            """, (album.numAlb,))
            morceaux = [
                Morceau(
                    numMorc=row[0],
                    titreMorceau=row[1],
                    duree=row[2],
                    paroles=row[3]
                )
                for row in cursor.fetchall()
            ]
    return render_template('album.html', album=album, morceaux=morceaux)

@main.route('/albums')
@login_required
def albums():
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dataset.album")
            albums = [
                Album(
                    numAlb=row[0],
                    titreAlbum=row[1],
                    dateParution=row[2],
                    description=row[4]
                )
                for row in cursor.fetchall()
            ]
    return render_template('album-catalog.html', albums=albums)

@main.route('/morceau/<int:morceau_id>')
@login_required
def morceau_page(morceau_id):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.morceau WHERE "numMorc" = %s', (morceau_id,))
            morceau_data = cursor.fetchone()
            if not morceau_data:
                flash("Morceau non trouvé", 'danger')
                return redirect(url_for('main.home'))
    morceau = Morceau(
        numMorc=morceau_data[0],
        titreMorceau=morceau_data[1],
        duree=morceau_data[2],
        paroles=morceau_data[3]
    )
    
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT a.nom, a.prenom, ad.role
            FROM dataset.artiste a
            JOIN dataset.apparait_dans ad ON a."numArt" = ad."numArt"
            WHERE ad."numMorc" = %s
            """, (morceau.numMorc,))
            artistes = [
                {
                    'nom': row[0],
                    'prenom': row[1],
                    'role': row[2]
                }
                for row in cursor.fetchall()
            ]
            print(artistes)
    return render_template('music.html', morceau=morceau, artistes=artistes)

@main.route('/morceau/<int:morceau_id>/ecoute', methods=['POST'])
@login_required
def increment_ecoute(morceau_id):
    with connect() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute('SELECT * FROM dataset.morceau WHERE "numMorc" = %s', (morceau_id,))
                morceau_data = cursor.fetchone()
                if not morceau_data:
                    flash("Morceau non trouvé", 'danger')
                    print("Morceau non trouvé")
                    return redirect(url_for('main.home'))
                

                cursor.execute("""
                    INSERT INTO dataset.ecoute ("numUsr", "numMorc", "date", "nombreEcoute")
                    VALUES (%s, %s, %s, 1)
                    ON CONFLICT ("numUsr", "numMorc")
                    DO UPDATE SET "nombreEcoute" = dataset.ecoute."nombreEcoute" + 1,
                                "date" = EXCLUDED."date";
                """, (current_user.numUsr, morceau_id, datetime.now(timezone('Europe/Paris'))))
                print("Ecoute incrémentée")
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                flash("Une erreur s'est produite lors de l'incrémentation de l'écoute.", 'danger')
                print(f"Erreur lors de l'incrémentation de l'écoute : {e}")
                return redirect(url_for('main.home'))
    return redirect(url_for('main.morceau_page', morceau_id=morceau_id))

@main.route('/suggestions')
@login_required
def suggestions():
    user_id = current_user.numUsr

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT a."numArt", a."nom", a."prenom", SUM(e."nombreEcoute") AS total_ecoutes
                FROM dataset.artiste a
                JOIN dataset.apparait_dans ad ON a."numArt" = ad."numArt"
                JOIN dataset.ecoute e ON e."numMorc" = ad."numMorc"
                WHERE e."numUsr" = %s
                GROUP BY a."numArt"
                ORDER BY total_ecoutes DESC
            """, (user_id,))
            top_artistes = [
                {
                    'numArt': row[0],
                    'nom': row[1],
                    'prenom': row[2],
                    'total_ecoutes': row[3]
                } for row in cursor.fetchall()
            ]
        
            cursor.execute("""
            SELECT m."numMorc", m."titreMorceau", m."duree", 
                    array_agg(a."nom" || ' ' || a."prenom") AS artistes
                FROM dataset.morceau m
                JOIN dataset.apparait_dans ad ON m."numMorc" = ad."numMorc"
                JOIN dataset.artiste a ON ad."numArt" = a."numArt"
                WHERE ad."numArt" = ANY(%s)
                GROUP BY m."numMorc"
            """, ([artiste['numArt'] for artiste in top_artistes],))
            morceaux_suggeres = [
                {
                    'numMorc': row[0],
                    'titreMorceau': row[1],
                    'duree': row[2],
                    'artistes': row[3]
                }
                for row in cursor.fetchall()
            ]
    
            cursor.execute("""
            SELECT g."numGrp", g."nomGroupe", COUNT(pa."numArt") AS popularite
            FROM dataset.groupe g
            JOIN dataset.participe_a pa ON g."numGrp" = pa."numGrp"
            JOIN (
                SELECT DISTINCT ad."numArt"
                FROM dataset.ecoute e
                JOIN dataset.apparait_dans ad ON e."numMorc" = ad."numMorc"
                WHERE e."numUsr" = %s
            ) utilisateurs_similaires ON utilisateurs_similaires."numArt" = pa."numArt"
            GROUP BY g."numGrp"
            ORDER BY popularite DESC
            """, (user_id,))
            groupes_suggeres = [
                {
                    'numGrp': row[0],
                    'nomGroupe': row[1],
                    'popularite': row[2]
                }
                for row in cursor.fetchall()
            ]

            cursor.execute("""
            SELECT "idSuivi"
                FROM dataset.suit
                WHERE "idSuiveur" = %s AND "typeSuivi" = 'user_follow'
            """, (user_id,))
            suivis = [row[0] for row in cursor.fetchall()]

            cursor.execute("""
            SELECT p."numPlay", p."titrePlaylist", p."description", p."visibilite", c."dateCreation", c."numUsr", u."pseudonyme"
            FROM dataset.playlist p
            JOIN dataset.cree c ON p."numPlay" = c."numPlay"
            JOIN dataset.utilisateur u ON c."numUsr" = u."numUsr"
            WHERE c."numUsr" = ANY(%s)
            """, (suivis,))
            playlists_suggerees = [
                {
                    'numPlay': row[0],
                    'titrePlaylist': row[1],
                    'description': row[2],
                    'visibilite': row[3],
                    'dateCreation': row[4],
                    'numUsr': row[5],
                    'pseudonyme': row[6]
                }
                for row in cursor.fetchall()
            ]

    return render_template(
        'suggestion.html',
        morceaux_suggeres=morceaux_suggeres,
        top_artistes=top_artistes,
        groupes_suggeres=groupes_suggeres,
        playlists_suggerees=playlists_suggerees
    )

@main.route('/playlist/<int:playlist_id>')
@login_required
def playlist_page(playlist_id):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.playlist WHERE "numPlay" = %s', (playlist_id,))
            playlist_data = cursor.fetchone()
            if not playlist_data:
                flash("Playlist non trouvée", 'danger')
                return redirect(url_for('main.home'))
            playlist = Playlist(
                numPlay=playlist_data[0],
                titrePlaylist=playlist_data[1],
                visibilite=playlist_data[2],
                description=playlist_data[3]
            )
    
            cursor.execute("""
            SELECT u."numUsr", u."pseudonyme", u."email", u."motDePasse", u."dateInscription", c."dateCreation"
            FROM dataset.utilisateur u
            JOIN dataset.cree c ON u."numUsr" = c."numUsr"
            WHERE c."numPlay" = %s
            """, (playlist_id,))
            createur_data = cursor.fetchone()
            if createur_data:
                createur = {
                    'numUsr':createur_data[0],
                    'pseudonyme':createur_data[1],
                    'email':createur_data[2],
                    'motDePasse':createur_data[3],
                    'dateInscription':createur_data[4],
                    'dateCreation':createur_data[5]
                }
            else:
                createur = None
            
            cursor.execute("""
                SELECT m."numMorc", m."titreMorceau", m."duree", m."paroles", a."titreAlbum"
                FROM dataset.morceau m
                JOIN dataset.inclut i ON m."numMorc" = i."numMorc"
                JOIN dataset.contient c ON m."numMorc" = c."numMorc"
                JOIN dataset.album a ON c."numAlb" = a."numAlb"
                WHERE i."numPlay" = %s
                ORDER BY i."ordre"
            """, (playlist_id,))
            morceaux = [
                {
                    'numMorc': row[0],
                    'titreMorceau': row[1],
                    'duree': row[2],
                    'paroles': row[3],
                    'titreAlbum': row[4]
                }
                for row in cursor.fetchall()
            ]
                
    if playlist.visibilite == 'private' and (
        createur is None or createur['numUsr'] != current_user.numUsr
    ):
        flash("Vous n'avez pas le droit d'accès à cette playlist privée.", 'danger')
        print("L'utilisateur n'a pas le droit d'accès à cette playlist privée.")
        return redirect(request.referrer or url_for('main.home'))
    
    return render_template('playlist.html', playlist=playlist, createur=createur, morceaux=morceaux)

@main.route('/my-playlists')
@login_required
def user_playlists():
    user_id = current_user.numUsr
    playlists = []

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT p."numPlay", p."titrePlaylist", p."visibilite", p."description", c."dateCreation"
            FROM dataset.playlist p
            JOIN dataset.cree c ON p."numPlay" = c."numPlay"
            WHERE c."numUsr" = %s
            """, (user_id,))
            playlists = cursor.fetchall()

    playlists_data = [
        {
            'numPlay': row[0],
            'titrePlaylist': row[1],
            'visibilite': row[2],
            'description': row[3],
            'dateCreation': row[4]
        }
        for row in playlists
    ]

    return render_template('playlist-catalog.html', playlists=playlists_data)
