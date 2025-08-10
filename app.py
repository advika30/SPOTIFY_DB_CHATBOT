import os
import re
import sqlite3
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Missing GOOGLE_API_KEY in .env file. Please add it before running.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# ---------------------------------------------------
# 2. DB setup
# ---------------------------------------------------
DB_PATH = "spotify.db"

def get_schema(db_path):
    """Fetch schema info from SQLite DB."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    schema_str = "\n".join([f"{name}: {sql}" for name, sql in tables])
    return schema_str

# Cache schema
schema_info = get_schema(DB_PATH)

# ---------------------------------------------------
# 3. Run SQL queries
# ---------------------------------------------------
def run_query(query):
    """Run SQL query and return DataFrame or error string."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(query, conn)

        # Deduplicate column names in a safe way
        seen = {}
        new_cols = []
        for col in df.columns:
            if col not in seen:
                seen[col] = 0
                new_cols.append(col)
            else:
                seen[col] += 1
                new_cols.append(f"{col}_{seen[col]}")
        df.columns = new_cols

        return df
    except Exception as e:
        return str(e)


# ---------------------------------------------------
# 4. Streamlit UI
# ---------------------------------------------------
st.title("🎵 Spotify DB Chatbot (Gemini-powered)")

user_question = st.text_input("Ask me about artists, albums, or tracks:")

if st.button("Ask"):
    if not user_question.strip():
        st.warning("Please type a question first.")
    else:
        # Build Gemini prompt
        prompt = f"""
        You are an expert SQL assistant for a SQLite music database.
        Here is the schema of the database:
        {schema_info}

        IMPORTANT RULES:
        - Only use tables and columns that actually exist in this schema.
        - Always join tables in this exact order:
          artists
          → albums
          → tracks
        - Use JOIN conditions:
          * artists.artist_id = albums.artist_id
          * albums.album_id = tracks.album_id
        - Always give descriptive aliases for columns from different tables 
          (e.g., artist_name, album_title, track_title).
        - Do NOT use Markdown formatting, code fences, or triple backticks.
        - Return only the SQL query that answers the user question.

        Question: {user_question}
        SQL:
        """

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            gemini_response = model.generate_content(prompt)

            # Clean Gemini's output
            sql_query = gemini_response.text.strip()
            sql_query = re.sub(r"```[a-zA-Z]*", "", sql_query)  # remove ```sql or ```sqlite
            sql_query = sql_query.replace("```", "").strip()

            # Show generated SQL
            st.code(sql_query, language="sql")

            # Run query
            result = run_query(sql_query)
            if isinstance(result, pd.DataFrame):
                if not result.empty:
                    st.dataframe(result)
                else:
                    st.info("✅ Query ran successfully but returned no rows.")
            else:
                st.error(f"Error executing query: {result}")

        except Exception as e:
            st.error(f"Error calling Gemini API: {e}")
