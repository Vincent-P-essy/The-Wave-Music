from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the-wave-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/thewave'
    
    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Enregistrer les Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .db import connect
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM dataset.utilisateur WHERE "numUsr" = %s', (user_id))
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