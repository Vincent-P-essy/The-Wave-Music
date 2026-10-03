"""Create a local demo account without embedding its password in the source."""
import argparse
from getpass import getpass

from passlib.hash import bcrypt

from app.db import connect
from app.main import create_app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--email', default='demo@example.invalid')
    parser.add_argument('--name', default='demo')
    args = parser.parse_args()
    password = getpass('Mot de passe du compte de démonstration : ')
    if not password or password != getpass('Confirmer le mot de passe : '):
        parser.error('Le mot de passe doit être non vide et confirmé.')
    app = create_app()
    with app.app_context(), connect() as conn, conn.cursor() as cursor:
        cursor.execute('SELECT 1 FROM dataset.utilisateur WHERE email=%s OR pseudonyme=%s',
                       (args.email, args.name))
        if cursor.fetchone():
            parser.error('Ce compte existe déjà ; choisir une autre adresse et un autre nom.')
        cursor.execute(
            'INSERT INTO dataset.utilisateur (pseudonyme,email,"motDePasse","dateInscription") '
            'VALUES (%s,%s,%s,CURRENT_DATE)',
            (args.name, args.email, bcrypt.hash(password)),
        )
    print(f'Compte de démonstration créé : {args.email}')


if __name__ == '__main__':
    main()
