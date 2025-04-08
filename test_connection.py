import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read variables from .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
CONNECT_TIMEOUT = os.getenv("CONNECT_TIMEOUT")
LOCK_TIMEOUT = os.getenv("LOCK_TIMEOUT")

# Attempt to connect to the database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        connect_timeout=int(CONNECT_TIMEOUT),
        options=f"-c lock_timeout={LOCK_TIMEOUT}"
    )
    print("✅ Database connection successful!")
    conn.close()
except Exception as e:
    print("❌ Failed to connect to the database:", e)
