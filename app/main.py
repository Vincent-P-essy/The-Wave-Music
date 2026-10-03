import os
import secrets

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://postgres@localhost:5432/thewave'
    )
    if config:
        app.config.update(config)
    
    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Enregistrer les Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    if user_id < 1:
        return None
    from .db import connect
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.utilisateur WHERE "numUsr" = %s', (user_id,))
            user_data = cursor.fetchone()
    if user_data:
        from .models import Utilisateur
        user_data_dict = {
            'pseudonyme': user_data[0],
            'email': user_data[1],
            'motDePasse': user_data[2],
            'dateInscription': user_data[3],
            'numUsr': user_data[4]
        }
        return Utilisateur(**user_data_dict)
    return None

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
