"""Regression tests; PostgreSQL cases require a disposable imported demo database."""
import os
import secrets
import unittest
from unittest.mock import patch

import psycopg2
from passlib.hash import bcrypt

from app.main import create_app, load_user
from app.db import connect


class ConfigurationTests(unittest.TestCase):
    def test_environment_configures_the_application(self):
        with patch.dict(os.environ, {
            'DATABASE_URL': 'postgresql://demo@localhost:55432/thewave',
            'SECRET_KEY': secrets.token_hex(32),
        }):
            app = create_app()
            self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], os.environ['DATABASE_URL'])
            self.assertEqual(app.config['SECRET_KEY'], os.environ['SECRET_KEY'])

    def test_default_session_keys_are_generated_per_app(self):
        with patch.dict(os.environ, {'SECRET_KEY': ''}):
            self.assertNotEqual(create_app().secret_key, create_app().secret_key)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite://', 'TESTING': True})

    @patch('app.db.psycopg2.connect')
    def test_connection_is_closed_after_use(self, open_connection):
        with self.app.app_context(), connect() as connection:
            self.assertIs(connection, open_connection.return_value)
        connection.close.assert_called_once()

    @patch('app.db.psycopg2.connect')
    def test_connection_is_closed_after_failure(self, open_connection):
        with self.app.app_context(), self.assertRaisesRegex(ValueError, 'test failure'):
            with connect():
                raise ValueError('test failure')
        open_connection.return_value.close.assert_called_once()

    @patch('app.db.connect')
    def test_invalid_session_id_does_not_query_the_database(self, open_connection):
        for value in [None, '', 'invalid', '0', '-1']:
            self.assertIsNone(load_user(value))
        open_connection.assert_not_called()


@unittest.skipUnless(os.environ.get('TEST_DATABASE_URL'), 'Set TEST_DATABASE_URL to an imported demo database')
class PostgreSQLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = os.environ['TEST_DATABASE_URL']
        cls.password = secrets.token_urlsafe(24)
        cls.email = f'test-{secrets.token_hex(8)}@example.invalid'
        cls.user_id = 10000 + secrets.randbelow(1000000)
        cls.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': cls.url})
        with psycopg2.connect(cls.url) as conn, conn.cursor() as cursor:
            cursor.execute('INSERT INTO dataset.utilisateur ("numUsr",pseudonyme,email,"motDePasse","dateInscription") VALUES (%s,%s,%s,%s,CURRENT_DATE)',
                           (cls.user_id, 'Test account', cls.email, bcrypt.hash(cls.password)))
            cursor.execute('INSERT INTO dataset.playlist ("titrePlaylist",visibilite,description) VALUES (%s,%s,%s) RETURNING "numPlay"',
                           ('Private test playlist', 'private', 'Synthetic test data'))
            cls.playlist_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO dataset.cree ("numUsr","numPlay","dateCreation") VALUES (%s,%s,CURRENT_TIMESTAMP)', (cls.user_id, cls.playlist_id))

    @classmethod
    def tearDownClass(cls):
        with psycopg2.connect(cls.url) as conn, conn.cursor() as cursor:
            cursor.execute('DELETE FROM dataset.ecoute WHERE "numUsr"=%s', (cls.user_id,))
            cursor.execute('DELETE FROM dataset.cree WHERE "numPlay"=%s', (cls.playlist_id,))
            cursor.execute('DELETE FROM dataset.playlist WHERE "numPlay"=%s', (cls.playlist_id,))
            cursor.execute('DELETE FROM dataset.utilisateur WHERE "numUsr"=%s', (cls.user_id,))

    def setUp(self):
        self.client = self.app.test_client()
        self.client.post('/login', data={'email': self.email, 'password': self.password})

    def test_multi_digit_user_id_survives_the_next_request(self):
        response = self.client.get('/albums')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test account', response.data)

    def test_suggestions_without_listening_history(self):
        with psycopg2.connect(self.url) as conn, conn.cursor() as cursor:
            cursor.execute('DELETE FROM dataset.ecoute WHERE "numUsr"=%s', (self.user_id,))
        self.assertEqual(self.client.get('/suggestions').status_code, 200)

    def test_catalog_and_detail_pages(self):
        for path in ['/', '/albums', '/album/1', '/artistes', '/artiste/1', '/groupes', '/groupe/1', '/morceau/1', '/my-playlists', '/playlist/1']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_album_description_comes_from_the_text_column(self):
        with psycopg2.connect(self.url) as conn, conn.cursor() as cursor:
            cursor.execute('SELECT description FROM dataset.album WHERE "numAlb"=1')
            description = cursor.fetchone()[0]
        self.assertIn(description.encode(), self.client.get('/album/1').data)

    def test_private_playlist_is_accessible_to_its_owner(self):
        self.assertEqual(self.client.get(f'/playlist/{self.playlist_id}').status_code, 200)

    def test_private_playlist_is_refused_to_another_user(self):
        other = self.app.test_client()
        with other.session_transaction() as session:
            session['_user_id'] = '1'
            session['_fresh'] = True
        self.assertEqual(other.get(f'/playlist/{self.playlist_id}').status_code, 302)

    def test_listening_increments_and_unlocks_suggestions(self):
        with psycopg2.connect(self.url) as conn, conn.cursor() as cursor:
            cursor.execute('DELETE FROM dataset.ecoute WHERE "numUsr"=%s', (self.user_id,))
        self.assertEqual(self.client.post('/morceau/1/ecoute').status_code, 302)
        self.assertEqual(self.client.post('/morceau/1/ecoute').status_code, 302)
        with psycopg2.connect(self.url) as conn, conn.cursor() as cursor:
            cursor.execute('SELECT "nombreEcoute" FROM dataset.ecoute WHERE "numUsr"=%s AND "numMorc"=1', (self.user_id,))
            self.assertEqual(cursor.fetchone()[0], 2)
        self.assertEqual(self.client.get('/suggestions').status_code, 200)

    def test_logout_removes_access_to_the_catalog(self):
        self.client.post('/logout')
        self.assertEqual(self.client.get('/albums').status_code, 302)


if __name__ == '__main__':
    unittest.main()
