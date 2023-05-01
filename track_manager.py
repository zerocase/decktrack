import sqlite3
import db
from track import Track

class TrackManager:
    
    def __del__(self):
        db.conn.close()

    def add_track(self, track):
        cursor = db.conn.cursor()
        cursor.execute("""
        INSERT INTO tracks (title, artist, duration, key, bpm, loudness, danceability, energy, odir)
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
            track.odir
        ))
        db.conn.commit()

    def get_track_by_id(self, id):
        cursor = db.conn.cursor()
        cursor.execute("""
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, odir
        FROM tracks
        WHERE id=?
        """, (id,))
        row = cursor.fetchone()
        if row:
            return Track(*row)
        else:
            return None

    def get_all_tracks(self):
        cursor = db.conn.cursor()
        cursor.execute("""
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, odir
        FROM tracks
        """)
        rows = cursor.fetchall()
        return [Track(*row) for row in rows]

    def update_track(self, track):
        cursor = db.conn.cursor()
        cursor.execute("""
        UPDATE tracks
        SET title=?, artist=?, duration=?, key=?, bpm=?, loudness=?, danceability=?, energy=?, odir=?
        WHERE track_id=?
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
        db.conn.commit()

    def delete_track(self, track):
        cursor = db.conn.cursor()
        cursor.execute("""
        DELETE FROM tracks
        WHERE track_id=?
        """, (track.id,))
        db.conn.commit()
