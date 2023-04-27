import sqlite3
from track import Track

class TrackManager:
    def __init__(self, db_file ="data/track_data.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            artist TEXT,
            duration FLOAT,
            key INTEGER,
            bpm FLOAT,
            loudness FLOAT,
            danceability FLOAT,
            energy FLOAT,
            ldir TEXT
        )
        """)
        self.conn.commit()

    def add_track(self, track):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO tracks (title, artist, duration, key, bpm, loudness, danceability, energy, ldir)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            track.title,
            track.artist,
            track.duration,
            track.key,
            track.bpm,
            track.loudness,
            track.danceability,
            track.energy,
            track.ldir
        ))
        self.conn.commit()

    def get_track_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id, title, artist, duration, key, bpm, loudness, danceability, energy
        FROM tracks
        WHERE id=?
        """, (id,))
        row = cursor.fetchone()
        if row:
            return Track(*row)
        else:
            return None

    def get_all_tracks(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id, title, artist, duration, key, bpm, loudness, danceability, energy
        FROM tracks
        """)
        rows = cursor.fetchall()
        return [Track(*row) for row in rows]

    def update_track(self, track):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE tracks
        SET title=?, artist=?, duration=?, key=?, bpm=?, loudness=?, danceability=?, energy=?
        WHERE id=?
        """, (
            track.title,
            track.artist,
            track.duration,
            track.key,
            track.bpm,
            track.loudness,
            track.danceability,
            track.energy,
            track.id
        ))
        self.conn.commit()

    def delete_track(self, track):
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM tracks
        WHERE id=?
        """, (track.id,))
        self.conn.commit()
