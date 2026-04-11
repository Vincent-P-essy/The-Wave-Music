from datetime import datetime

from flask_login import UserMixin

from .main import db


class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateur'
    __table_args__ = {'schema': 'dataset'}

    numUsr = db.Column(db.Integer, primary_key=True)
    pseudonyme = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    motDePasse = db.Column(db.String, nullable=False)
    dateInscription = db.Column(db.Date, nullable=False)
    
    suit_suiveur = db.relationship('Suit', foreign_keys='Suit.idSuiveur', back_populates='suiveur', lazy='dynamic')
    suit_suivi = db.relationship('Suit', foreign_keys='Suit.idSuivi', back_populates='suivi', lazy='dynamic')
    ecoutes = db.relationship('Ecoute', back_populates='utilisateur', lazy=True)
    creations = db.relationship('Cree', back_populates='utilisateur')

    def __repr__(self):
        return f'<Utilisateur {self.pseudonyme}>'
    
    def get_id(self):
        return str(self.numUsr)

    def verify_password(self, password):
        return self.motDePasse == password
    
class Morceau(db.Model):
    __tablename__ = 'morceau'
    __table_args__ = {'schema': 'dataset'}

    numMorc = db.Column(db.Integer, primary_key=True)
    titreMorceau = db.Column(db.String, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    paroles = db.Column(db.Text)

    # Définition de la relation vers la table de jointure 'ApparaîtDans'
    apparait_dans = db.relationship('ApparaitDans', back_populates='morceau')
    albums_associes = db.relationship('Contient', back_populates='morceau', cascade="all, delete-orphan")
    ecoutes = db.relationship('Ecoute', back_populates='morceau', lazy=True)

    def __repr__(self):
        return f'<Morceau {self.titreMorceau}>'

class Artiste(db.Model):
    __tablename__ = 'artiste'
    __table_args__ = {'schema': 'dataset'}

    numArt = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    prenom = db.Column(db.String, nullable=False)
    nationalite = db.Column(db.String, nullable=False)
    dateNaissance = db.Column(db.Date, nullable=False)
    dateDeces = db.Column(db.Date)

    # Définition de la relation vers la table de jointure 'ApparaîtDans'
    apparait_dans = db.relationship('ApparaitDans', back_populates='artiste')
    participations = db.relationship('ParticipeA', back_populates='artiste', lazy='dynamic')


    def __repr__(self):
        return f'<Artiste {self.nom} {self.prenom}>'

class ApparaitDans(db.Model):
    __tablename__ = 'apparait_dans'
    __table_args__ = {'schema': 'dataset'}

    numArt = db.Column(db.Integer, db.ForeignKey('dataset.artiste.numArt'), primary_key=True)
    numMorc = db.Column(db.Integer, db.ForeignKey('dataset.morceau.numMorc'), primary_key=True)
    role = db.Column(db.Integer, nullable=False, primary_key=True)

    # Relation vers le modèle Artiste
    artiste = db.relationship('Artiste', back_populates='apparait_dans')

    # Relation vers le modèle Morceau
    morceau = db.relationship('Morceau', back_populates='apparait_dans')

    def __repr__(self):
        return f'<ApparaitDans {self.artiste.nom} - {self.morceau.titreMorceau}>'

class Album(db.Model):
    __tablename__ = 'album'
    __table_args__ = {'schema': 'dataset'}

    numAlb = db.Column(db.Integer, primary_key=True)
    titreAlbum = db.Column(db.String, nullable=False)
    dateParution = db.Column(db.Date, nullable=False)
    imageCouverture = db.Column(db.LargeBinary)  # Pour l'image
    description = db.Column(db.Text)
    
    publie_groupes = db.relationship('Publie', back_populates='album', lazy='dynamic')
    morceaux_associes = db.relationship('Contient', back_populates='album', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Album {self.titreAlbum}>'

class Playlist(db.Model):
    __tablename__ = 'playlist'
    __table_args__ = {'schema': 'dataset'}

    numPlay = db.Column(db.Integer, primary_key=True)
    titrePlaylist = db.Column(db.String, nullable=False)
    visibilite = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    
    createurs = db.relationship('Cree', back_populates='playlist')

    def __repr__(self):
        return f'<Playlist {self.titrePlaylist}>'
    
class Groupe(db.Model):
    __tablename__ = 'groupe'
    __table_args__ = {'schema': 'dataset'}

    numGrp = db.Column(db.Integer, primary_key=True)
    nomGroupe = db.Column(db.String, nullable=False)
    dateCreation = db.Column(db.Date)
    nationalite = db.Column(db.String)
    gerneMusical = db.Column(db.String)
    
    membres = db.relationship('ParticipeA', back_populates='groupe', lazy='dynamic')
    publie_albums = db.relationship('Publie', back_populates='groupe', lazy='dynamic')

    def __repr__(self):
        return f'<Groupe {self.nomGroupe}>'
    
class Suit(db.Model):
    __tablename__ = 'suit'
    __table_args__ = {'schema': 'dataset'}

    idSuiveur = db.Column(db.Integer, db.ForeignKey('dataset.utilisateur.numUsr'), primary_key=True)
    idSuivi = db.Column(db.Integer, db.ForeignKey('dataset.utilisateur.numUsr'), primary_key=True)
    typeSuivi = db.Column(db.String, nullable=False)

    suiveur = db.relationship('Utilisateur', foreign_keys=[idSuiveur], back_populates='suit_suiveur')
    suivi = db.relationship('Utilisateur', foreign_keys=[idSuivi], back_populates='suit_suivi')

    def __repr__(self):
        return f'<Suit {self.suiveur.pseudonyme} suit {self.suivi.pseudonyme}>'
    
class ParticipeA(db.Model):
    __tablename__ = 'participe_a'
    __table_args__ = {'schema': 'dataset'}

    numArt = db.Column(db.Integer, db.ForeignKey('dataset.artiste.numArt'), primary_key=True)
    numGrp = db.Column(db.Integer, db.ForeignKey('dataset.groupe.numGrp'), primary_key=True)
    role = db.Column(db.String, nullable=False, primary_key=True)  # Inclure `role` comme clé primaire
    dateEntree = db.Column(db.Date, nullable=True)
    dateSortie = db.Column(db.Date, nullable=True)

    # Relations
    artiste = db.relationship('Artiste', back_populates='participations')
    groupe = db.relationship('Groupe', back_populates='membres')

    def __repr__(self):
        return f'<ParticipeA Artiste={self.numArt}, Groupe={self.numGrp}, Rôle={self.role}>'
    
class Publie(db.Model):
    __tablename__ = 'publie'
    __table_args__ = {'schema': 'dataset'}

    numGrp = db.Column(db.Integer, db.ForeignKey('dataset.groupe.numGrp'), primary_key=True)
    numAlb = db.Column(db.Integer, db.ForeignKey('dataset.album.numAlb'), primary_key=True)

    # Relations
    groupe = db.relationship('Groupe', back_populates='publie_albums')
    album = db.relationship('Album', back_populates='publie_groupes')
    
class Contient(db.Model):
    __tablename__ = 'contient'
    __table_args__ = {'schema': 'dataset'}

    numAlb = db.Column(db.Integer, db.ForeignKey('dataset.album.numAlb'), primary_key=True)
    numMorc = db.Column(db.Integer, db.ForeignKey('dataset.morceau.numMorc'), primary_key=True)
    ordre = db.Column(db.Integer, nullable=False)
    
    album = db.relationship('Album', back_populates='morceaux_associes')
    morceau = db.relationship('Morceau', back_populates='albums_associes')

    def __repr__(self):
        return f'<Contient {self.numAlb} - {self.numMorc}>'
    

class Ecoute(db.Model):
    __tablename__ = 'ecoute'
    __table_args__ = {'schema': 'dataset'}

    numUsr = db.Column(db.Integer, db.ForeignKey('dataset.utilisateur.numUsr'), primary_key=True)  # User ID
    numMorc = db.Column(db.Integer, db.ForeignKey('dataset.morceau.numMorc'), primary_key=True)  # Song ID
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of listen
    nombreEcoute = db.Column(db.Integer, nullable=False, default=1)  # Number of listens

    # Relationships with other tables
    utilisateur = db.relationship('Utilisateur', back_populates='ecoutes', lazy=True)
    morceau = db.relationship('Morceau', back_populates='ecoutes', lazy=True)

    def __init__(self, numUsr, numMorc, date=None, nombreEcoute=1):
        self.numUsr = numUsr
        self.numMorc = numMorc
        self.date = date if date else datetime.now().astimezone()
        self.nombreEcoute = nombreEcoute

    def __repr__(self):
        return f'<Ecoute {self.numUsr} {self.numMorc} {self.nombreEcoute}>'
    
class Cree(db.Model):
    __tablename__ = 'cree'
    __table_args__ = {'schema': 'dataset'}
    
    numUsr = db.Column(db.Integer, db.ForeignKey('dataset.utilisateur.numUsr'), primary_key=True, nullable=False)
    numPlay = db.Column(db.Integer, db.ForeignKey('dataset.playlist.numPlay'), primary_key=True, nullable=False)
    dateCreation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    utilisateur = db.relationship('Utilisateur', back_populates='creations')
    playlist = db.relationship('Playlist', back_populates='createurs')

    def __init__(self, numUsr, numPlay, dateCreation=None):
        self.numUsr = numUsr
        self.numPlay = numPlay
        self.dateCreation = dateCreation if dateCreation else datetime.utcnow()

    def __repr__(self):
        return f'<Cree {self.numUsr} {self.numPlay} {self.dateCreation}>'