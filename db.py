import sqlite3


db_file ="data/decktrack.db"
conn = sqlite3.connect(db_file) 


def create_collections_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS collections
                    (
                        collection_id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      collection_type TEXT NOT NULL,
                      tracklist_ids TEXT NOT NULL)''')
    conn.commit()


def create_tracks_table():
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id INTEGER PRIMARY KEY,
            title TEXT,
            artist TEXT,
            duration FLOAT,
            key INTEGER,
            bpm FLOAT,
            loudness FLOAT,
            danceability FLOAT,
            energy FLOAT,
            odir TEXT
        )
        """)
    conn.commit()

def create_relations_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY,
            collection_id INTEGER,
            track_id INTEGER,
            FOREIGN KEY(collection_id) REFERENCES collections(collection_id),
            FOREIGN KEY(track_id) REFERENCES tracks(track_id)
        )""")
    conn.commit()

def initialize_tables():
    create_tracks_table()
    create_collections_table()
    create_relations_table()