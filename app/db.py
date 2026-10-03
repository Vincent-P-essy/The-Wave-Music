from contextlib import contextmanager

import psycopg2
from flask import current_app


@contextmanager
def connect():
    """Use the application's database and close each connection after use."""
    conn = psycopg2.connect(current_app.config['SQLALCHEMY_DATABASE_URI'])
    conn.autocommit = True
    try:
        yield conn
    finally:
        conn.close()
