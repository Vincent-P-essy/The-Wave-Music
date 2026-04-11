#  The Wave — Plateforme musicale open-source

**The Wave** est une plateforme musicale développée avec Python, Flask et PostgreSQL. Elle permet aux utilisateurs de découvrir, écouter et gérer de la musique via une interface web dynamique.

---

##  Fonctionnalités

-  Connexion / inscription utilisateur
-  Visualisation de musique, playlists, artistes...
-  Backend en Flask avec SQLAlchemy
-  Base de données PostgreSQL (fichier `.sql` fourni)
-  Authentification avec Flask-Login
-  Interface web HTML/CSS dynamique

---

##  Structure du projet
```
The-Wave-Music/
├── app/ # Code principal de l'application (routes, models, etc.)
├── instance/ # Configs spécifiques à l'environnement (facultatif)
├── requirements.txt # Dépendances Python
├── thewave-*.sql # Dump PostgreSQL complet
└── README.md # Ce fichier
```

---

##  Prérequis

- Python 3.10+
- PostgreSQL installé et accessible en local
- pip, venv

---

##  Installation & Lancement

1. Cloner ce dépôt :

```bash
git clone https://github.com/Vincent-P-essy/The-Wave-Music.git
cd The-Wave-Music
``` 

Créer et activer un environnement virtuel :
python3 -m venv venv
source venv/bin/activate
Installer les dépendances :
pip install -r requirements.txt
Créer la base PostgreSQL :
createdb thewave
Importer la structure + données :
psql -U postgres -d thewave -f thewave-2024_12_11_21_42_00-dump.sql

(Vous pouvez adapter le nom du fichier .sql si besoin)

Configurer les variables d'environnement :
export FLASK_APP=app.main:create_app
export FLASK_ENV=development
export DATABASE_URL=postgresql://postgres:password@localhost/thewave

(Remplacer password par votre mot de passe PostgreSQL)

Lancer le serveur Flask :
flask run
Accéder à l'application :

http://127.0.0.1:5000

Auteur

Développé par Vincent Plessy — github.com/Vincent-P-essy
