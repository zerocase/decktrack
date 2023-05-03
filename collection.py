from track import Track

class Collection:
    
    def __init__(self, name, collection_type):
        self.collection_id = None
        self.name = name
        self.collection_type = collection_type

    def get_name(self):
        return self.name

    def get_type(self):
        return self.collection_type