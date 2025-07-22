import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_CONFIG

# Connexion PostgreSQL avec curseur dictionnaire
def get_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

# Exécution d'une requête SELECT (avec résultat sous forme de liste de dictionnaires)
def fetch_all(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()

# Exécution d'une requête SELECT qui retourne un seul enregistrement
def fetch_one(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchone()

# Exécution d'une requête INSERT/UPDATE/DELETE
def execute_query(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()

# Insertion + récupération de l'id généré (utile pour créer une transaction, etc.)
def execute_and_return_id(query, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            last_id = cur.fetchone()[0]
            conn.commit()
            return last_id

