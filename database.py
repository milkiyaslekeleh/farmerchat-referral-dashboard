import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

def get_connection():
    """Establishes and returns a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

def run_query(sql: str, params=None) -> pd.DataFrame:
    """Executes SQL query and returns results as a pandas DataFrame."""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params or ())
            data = cursor.fetchall()
            return pd.DataFrame(data)
    except Exception as e:
        print("Query error:", e)
        return pd.DataFrame()
    finally:
        conn.close()
