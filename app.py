import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="DA Referral Dashboard", layout="wide")

st.title("📊 DA Referral Summary Dashboard")

# DB connection
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            connect_timeout=int(os.getenv("CONNECT_TIMEOUT"))
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Query
def load_data():
    query = """
        SELECT 
            ud.full_name AS "DA Name",
            ud.phone AS "DA Phone",
            COUNT(umd.message_id) AS "Total Questions"
        FROM user_management_userprofile ump
        JOIN users_data_view ud ON ump.user_id_id = ud.user_id
        JOIN user_messages_data umd ON ump.user_id_id = umd.user_id
        WHERE ump.role = 'role_selection_all_extension_worker'
          AND ump.country_id = (SELECT id FROM geography_country WHERE name = 'Ethiopia')
          AND (umd.original_message IS NOT NULL OR umd.input_type IN ('image', 'voice', 'text'))
        GROUP BY ud.full_name, ud.phone
        ORDER BY "Total Questions" DESC
        LIMIT 50;
    """
    conn = get_connection()
    if conn:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()

# Display
with st.spinner("Loading data..."):
    data = load_data()

if not data.empty:
    st.success("Data loaded successfully!")
    st.dataframe(data, use_container_width=True)
    st.download_button("Download CSV", data.to_csv(index=False), "referral_summary.csv")
else:
    st.warning("No data found or connection error.")
