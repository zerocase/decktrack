import sqlite3
import db
from collection import Collection
from track import Track

class CollectionManager:  
    def __init__(self):
        self.conn = db.conn

    #def __del__(self):
    #    db.conn.close()

    def add_collection(self, collection):
        c = db.conn.cursor()
        c.execute("INSERT INTO collections (name, collection_type) VALUES (?, ?)",
                  (collection.get_name(), collection.get_type()))
        db.conn.commit()
        cid = c.lastrowid
        collection.collection_id = cid
    
    def get_collection_by_name(self, collection_name):
        c = db.conn.cursor()
        c.execute("""SELECT collection_id, name, collection_type
                     FROM collections WHERE name =?""", (collection_name,))
        row = c.fetchone()
        #print(row)
        if row:
            return row
        else:
            return None

    def remove_collection(self, collection_info):
        c = db.conn.cursor()
        c.execute("DELETE FROM collections WHERE collection_id=?", (collection_info[0],))
        db.conn.commit()

    def get_track_id_from_collection(self, collection_info):
        c = db.conn.cursor()
        c.execute("SELECT track_id FROM relations WHERE collection_id=?", (collection_info[0],))
        rows = c.fetchall()
        if rows:
            return rows
        else:
            return None
       

    def remove_collection_relations(self, collection_info):
        c = db.conn.cursor()
        c.execute("DELETE FROM relations WHERE collection_id=?", (collection_info[0],))
        db.conn.commit()

    def add_track_to_collection(self, collection, track):
        c = db.conn.cursor()
        c.execute("INSERT INTO relations (collection_id, track_id) VALUES (?, ?)",
                  (collection.collection_id, track.track_id))
        db.conn.commit()
    
    def get_collections(self):
        c = db.conn.cursor()
        names = [name[0] for name in c.execute("SELECT name FROM collections")]
        return names
    
    def get_tracks_by_collection_name(self, name):
        c = db.conn.cursor()
        c.execute('''SELECT title, artist, duration, key, bpm, loudness, danceability, energy, quality  from tracks t 
                    INNER JOIN
                    relations r  on t.track_id = r.track_id
                    INNER JOIN
                    collections c on c.collection_id = r.collection_id
                    WHERE name = ?''', (name,))
        rows = c.fetchall()
        return rows

    def get_track_ids_by_collection_id(self, collection_id):
        c = db.conn.cursor()
        c.execute('''SELECT track_id from relations WHERE collection_id = ?''', (collection_id,))
        rows = c.fetchall()
        return rows


    def get_tracks_by_collection_name_full(self, name):
        c = db.conn.cursor()   
        c.execute('''SELECT track_id, title, artist, duration, key, bpm, loudness, danceability, energy, quality, odir from tracks t
                     INNER JOIN
                     relations r  on t.track_id = r.track_id
                     INNER JOIN
                     collections c on c.collection_id = r.collection_id
                     WHERE name = ?''', (name,))
        rows = c.fetchall()
        return rows


