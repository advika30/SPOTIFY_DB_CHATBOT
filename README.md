# 🎵 Spotify DB Chatbot (Gemini-Powered)

A Streamlit app that lets you query a **Spotify-style music database** using **natural language** — no SQL skills required!  
Built with **Google Gemini**, it automatically converts your questions into SQL, runs them against a local SQLite database, and displays the results in a clean, interactive table.


## 🚀 Features

- **Natural Language to SQL**: Ask questions like *"Show all Jazz artists from India"* or *"Top 5 most streamed tracks"* and get instant answers.
- **Real Schema Awareness**: Gemini reads the actual SQLite schema at app startup to avoid hallucinating non-existent columns.
- **Pretty Table Output**: Results are displayed using Streamlit’s interactive dataframe viewer.
- **Consistent JOINs**: Always uses the correct table relationships:
  - `artists.artist_id → albums.artist_id`
  - `albums.album_id → tracks.album_id`
- **.env Support**: Securely store your Google API key.

---


## 🛠️ Setup Instructions

### Clone the repository
```bash
git clone https://github.com/yourusername/spotify-gemini-agent.git
cd spotify-gemini-agent
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python create_db.py
GOOGLE_API_KEY=your_google_api_key_here
streamlit run app.py
```

### 💡 Example Prompts
Try these in the app:

Top 5 most streamed tracks

List the top 5 most streamed tracks along with the artist name, album title, and stream count.

Filter by genre & country

Show all Jazz artists from India along with their albums and track titles.

Aggregate data

For each artist, show their total number of tracks and total streams, sorted by total streams in descending order.

## How It Works
On startup, the app reads the real SQLite schema (artists, albums, tracks) and passes it to Gemini.

Gemini receives:

The schema

The relationships between tables

The user’s question

Gemini generates valid SQL that matches the schema.

The SQL query is run against spotify.db.

Results are displayed as a pretty, scrollable table.

## 📸 Demo
(Add a GIF or screenshot here)

## 📜 License
MIT License — feel free to fork and build on this project.

## 💬 Acknowledgements
Google Gemini API

Streamlit

SQLite

Faker for synthetic data
