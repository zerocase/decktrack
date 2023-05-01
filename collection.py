from track import Track

class Collection:
    
    def __init__(self, collection_id, name, collection_type, tracklist_ids):
        self.collection_id = collection_id
        self.name = name
        self.collection_type = collection_type
        self.tracklist_ids = tracklist_ids

    def get_name(self):
        return self.name

    def get_type(self):
        return self.collection_type
    
    def get_tracklist(self):
        return self.tracklist_ids