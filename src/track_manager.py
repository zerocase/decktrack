import sqlite3
import db
from track import Track

class TrackManager:
    
    #def __del__(self):
    #    db.conn.close()

    def add_track(self, track):
        c = db.conn.cursor()
        c.execute("""
        INSERT INTO tracks (track_id, title, artist, duration, key, bpm, loudness, danceability, energy, quality, odir)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            track.track_id,
            track.title,
            track.artist,
            track.duration,
            track.key,
            track.bpm,
            track.loudness,
            track.danceability,
            track.energy,
            track.quality,
            track.odir
        ))
        tid = c.lastrowid
        track.track_id = tid
        db.conn.commit()

    def get_track_by_title_artist(self, title, artist):
        c = db.conn.cursor()
        c.execute("""
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, quality, odir
        FROM tracks
        WHERE title=? and artist=?
        """, (title, artist))
        row = c.fetchone()
        if row:
            return row
        else:
            return None

    def get_track_by_id(self, id):
        c = db.conn.cursor()
        c.execute("""
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, quality, odir
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
        SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, quality, odir
        FROM tracks
        """)
        rows = c.fetchall()
        return [Track(*row) for row in rows]

    def update_track(self, track, track_id):
        c = db.conn.cursor()
        c.execute("""
        UPDATE tracks
        SET title=?, artist=?, duration=?, key=?, bpm=?, loudness=?, danceability=?, energy=?, quality=?, odir=?
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
            track.quality,
            track.odir,
            track_id
        ))
        db.conn.commit()

    def delete_track(self, track_id):
        c = db.conn.cursor()
        c.execute("DELETE FROM tracks WHERE track_id=?", (track_id,))
        db.conn.commit()

    def delete_track_by_id(self, track_id):
        c = db.conn.cursor()
        c.execute("""
        DELETE FROM tracks
        WHERE track_id=?
        """, (track_id,))
        db.conn.commit()

    def get_odir(self, track):
        c = db.conn.cursor()
        c.execute("""
        SELECT odir
        FROM tracks
        WHERE track_id=?
        """, (track.track_id,))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            return None