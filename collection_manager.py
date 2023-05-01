import sqlite3
import db
from collection import Collection

class CollectionManager:  

    def __del__(self):
        db.conn.close()

    
    def add_collection(self, collection):
        c = db.conn.cursor()
        c.execute("INSERT INTO collections (name, collection_type, tracklist_ids) VALUES (?, ?, ?)",
                  (collection.get_name(), collection.get_type(), collection.get_tracklist()))
        db.conn.commit()
    
    def remove_collection(self, collection):
        c = db.conn.cursor()
        c.execute("DELETE FROM collections WHERE collection_id=?", (collection.collection_id,))
        db.conn.commit()

    def add_track_to_collection(self, collection, track):
        c = db.conn.cursor()
        c.execute("INSERT INTO relations (collection_id, track_id) VALUES (?, ?)",
                  (collection.collection_id, track.track_id))
        db.conn.commit()