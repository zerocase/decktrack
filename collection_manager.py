import sqlite3

from collection import Collection

class CollectionManager:
    def __init__(self, db_file ="data/collection_data.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.create_table()
    
    def __del__(self):
        self.conn.close()
    
    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS collections
                     (
                        id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      collection_type TEXT NOT NULL,
                      tracklist_ids TEXT NOT NULL)''')
        self.conn.commit()
    
    def add_collection(self, collection):
        c = self.conn.cursor()
        c.execute("INSERT INTO collections (name, collection_type, tracklist_ids) VALUES (?, ?, ?)",
                  (collection.get_name(), collection.get_type(), collection.get_tracklist()))
        self.conn.commit()
    
    def remove_collection(self, collection):
        c = self.conn.cursor()
        c.execute("DELETE FROM collections WHERE id=?", (collection.id))
        self.conn.commit()
    
    