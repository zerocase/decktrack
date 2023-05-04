import sqlite3
import db
from collection import Collection

class CollectionManager:  

    def __del__(self):
        db.conn.close()
    
    def add_collection(self, collection):
        c = db.conn.cursor()
        c.execute("INSERT INTO collections (name, collection_type) VALUES (?, ?)",
                  (collection.get_name(), collection.get_type()))
        db.conn.commit()
        cid = c.lastrowid
        collection.collection_id = cid
    
    def remove_collection(self, collection):
        c = db.conn.cursor()
        c.execute("DELETE FROM collections WHERE collection_id=?", (collection.collection_id,))
        db.conn.commit()

    def add_track_to_collection(self, collection, track):
        c = db.conn.cursor()
        c.execute("INSERT INTO relations (collection_id, track_id) VALUES (?, ?)",
                  (collection.collection_id, track.track_id))
        db.conn.commit()
    
    def get_collections(self):
        c = db.conn.cursor()
        c.execute("SELECT name FROM collections;")
        rows = c.fetchall()
        for row in rows:
            print(row)
