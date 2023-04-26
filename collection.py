from track import Track

class Collection:
    def __init__(self, name, collection_type, track_ids, conn):
        self.id = None
        self.name = name
        self.collection_type = collection_type
        self.track_ids = track_ids
        self.conn = conn


    def get_name(self):
        return self.name

    def get_collection(self):
        return self.collection_type

    def get_track_ids(self, conn):
        c = conn.cursor()
        c.execute("SELECT track_id FROM collections_tracks WHERE collection_id = ?", (self.id,))
        results = c.fetchall()
        track_ids = [result[0] for result in results]
        return track_ids
    
    def get_tracks(self, conn):
        track_ids = self.get_track_ids(conn)
        tracks = []
        for track_id in track_ids:
            c = conn.cursor()
            c.execute("SELECT * FROM tracks WHERE id=?", (track_id,))
            result = c.fetchone()
            track = Track(*result[1:])
            tracks.append(track)
        return tracks