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

\`\`\`
the-wave-music/
├── app/                  # Code principal de l'application (routes, models, etc.)
├── instance/             # Configs spécifiques à l'environnement (facultatif)
├── requirements.txt      # Dépendances Python
├── thewave-*.sql         # Dump PostgreSQL complet
└── README.md             # Ce fichier
\`\`\`

---

##  Prérequis

- Python 3.10+
- PostgreSQL installé et accessible en local
- pip, venv

---

##  Installation & Lancement

1. Cloner ce dépôt :

\`\`\`bash
git clone https://github.com/Vincent-P-essy/the-wave-music.git
cd the-wave-music
\`\`\`

2. Créer et activer un environnement virtuel :

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

3. Installer les dépendances :

\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Créer la base PostgreSQL :

\`\`\`bash
createdb -h localhost -U postgres thewave
\`\`\`

5. Importer la structure + données :

\`\`\`bash
psql -h localhost -U postgres -d thewave -f thewave-2024_12_11_21_42_00-dump.sql
\`\`\`

6. Lancer le serveur Flask :

\`\`\`bash
export FLASK_APP=app.main:create_app
export FLASK_ENV=development
flask run
\`\`\`

7. Accèder à l'application :

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

##  Auteur

Développé par Vincent Plessy — [github.com/Vincent-P-essy](https://github.com/Vincent-P-essy)

---

##  Licence

Voir fichier `LICENSE`.
