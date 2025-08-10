import sqlite3
import pandas as pd
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Connect to SQLite
conn = sqlite3.connect("spotify.db")
cursor = conn.cursor()

# Drop old tables if exist
cursor.execute("DROP TABLE IF EXISTS tracks;")
cursor.execute("DROP TABLE IF EXISTS albums;")
cursor.execute("DROP TABLE IF EXISTS artists;")

# Create tables
cursor.execute("""
CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    genre TEXT,
    country TEXT
);
""")

cursor.execute("""
CREATE TABLE albums (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER,
    title TEXT,
    release_year INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);
""")

cursor.execute("""
CREATE TABLE tracks (
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER,
    title TEXT,
    duration_sec INTEGER,
    streams INTEGER,
    FOREIGN KEY (album_id) REFERENCES albums(album_id)
);
""")

# Generate synthetic data
genres = ["Pop", "Rock", "Hip-Hop", "Jazz", "Classical"]
countries = ["USA", "UK", "India", "Canada", "Australia"]

# Insert artists
artist_ids = []
for _ in range(10):
    cursor.execute("""
    INSERT INTO artists (name, genre, country) VALUES (?, ?, ?)
    """, (fake.name(), random.choice(genres), random.choice(countries)))
    artist_ids.append(cursor.lastrowid)

# Insert albums
album_ids = []
for artist_id in artist_ids:
    for _ in range(random.randint(1, 3)):
        cursor.execute("""
        INSERT INTO albums (artist_id, title, release_year) VALUES (?, ?, ?)
        """, (artist_id, fake.word().title() + " Album", random.randint(2000, 2025)))
        album_ids.append(cursor.lastrowid)

# Insert tracks
for album_id in album_ids:
    for _ in range(random.randint(3, 7)):
        cursor.execute("""
        INSERT INTO tracks (album_id, title, duration_sec, streams) VALUES (?, ?, ?, ?)
        """, (
            album_id,
            fake.word().title(),
            random.randint(120, 300),
            random.randint(1000, 1000000)
        ))

# Commit and close
conn.commit()
conn.close()

print("Database created successfully!")
