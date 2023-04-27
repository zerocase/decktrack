import sqlite3
from collection import Collection

class CollectionManager:
    def __init__(self, db_file="data/track_database.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS collections
                     (id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      collection_type TEXT NOT NULL)''')

        c.execute('''CREATE TABLE IF NOT EXISTS tracks
                     (id INTEGER PRIMARY KEY,
                      title TEXT,
                      artist TEXT,
                      duration INTEGER)''')

        c.execute('''CREATE TABLE IF NOT EXISTS collections_tracks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      collection_id INTEGER,
                      track_id INTEGER,
                      FOREIGN KEY(collection_id) REFERENCES collections(id),
                      FOREIGN KEY(track_id) REFERENCES tracks(id))''')
        self.conn.commit()

    def add_collection(self, collection):
        c = self.conn.cursor()
        c.execute("INSERT INTO collections (name, collection_type, track_ids) VALUES (?, ?, ?)",
                  (collection.get_name(), collection.get_collection(), ",".join(collection.get_track_ids(self.conn))))
        self.conn.commit()
        collection_id = c.lastrowid
        collection.id = collection_id

    def remove_collection(self, collection):
        c = self.conn.cursor()
        c.execute("DELETE FROM collections WHERE id=?", (collection.id,))
        self.conn.commit()

    def get_collections(self):
        c = self.conn.cursor()
        c.execute("SELECT id, name, collection_type, track_ids FROM collections")
        rows = c.fetchall()
        collections = []
        for row in rows:
            collection_id, name, collection_type, track_ids = row
            collection = Collection(name, collection_type, track_ids.split(","))
            collection.id = collection_id
            collections.append(collection)
        return collections

    def get_collection(self, name):
        c = self.conn.cursor()
        c.execute("SELECT id, collection_type, track_ids FROM collections WHERE name=?", (name,))
        row = c.fetchone()
        if row is None:
            return None
        else:
            collection_id, collection_type, track_ids = row
            collection = Collection(name, collection_type, track_ids.split(","))
            collection.id = collection_id
            return collection

    def get_collection_by_id(self, id):
        c = self.conn.cursor()
        c.execute("SELECT name, collection_type, track_ids FROM collections WHERE id=?", (id,))
        result = c.fetchone()
        if result is None:
            return None
        name, collection_type, track_ids = result
        return Collection(name, collection_type, track_ids.split(","), self.conn)
    
    def get_track_ids(self, conn):
        c = conn.cursor()
        c.execute("SELECT track_ids FROM collections WHERE id=?", (self.id,))
        result = c.fetchone()
        if result:
            track_ids_str = result[0]
            return track_ids_str.split(",") if track_ids_str else []
        else:
            return []

    def clear_collections(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM collections")
        self.conn.commit()

    def close(self):
        self.conn.close()