import sqlite3
import db
from track import Track

class TrackManager:
    
    def __del__(self):
        db.conn.close()

    def add_track(self, track):
        c = db.conn.cursor()
        c.execute("""
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
        tid = c.lastrowid
        track.track_id = tid


    def get_track_by_id(self, id):
        c = db.conn.cursor()
        c.execute("""
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, odir
        FROM tracks
        WHERE id=?
        """, (id,))
        row = c.fetchone()
        if row:
            return Track(*row)
        else:
            return None

    def get_all_tracks(self):
        c = db.conn.cursor()
        c.execute("""
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, odir
        FROM tracks
        """)
        rows = c.fetchall()
        return [Track(*row) for row in rows]

    def update_track(self, track):
        c = db.conn.cursor()
        c.execute("""
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
            track.track_id
        ))
        db.conn.commit()

    def delete_track(self, track):
        c = db.conn.cursor()
        c.execute("""
        DELETE FROM tracks
        WHERE track_id=?
        """, (track.track_id,))
        db.conn.commit()
