import psycopg2


def connect():
    try:
        conn = psycopg2.connect(
            dbname="thewave",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None