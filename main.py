from track_manager import TrackManager
from collection_manager import CollectionManager
from track import Track
from collection import Collection

if __name__ == '__main__':
    pass
#    track_manager = TrackManager()    
#    track_manager.add_track(Track("Track 1", "Artist 1", 180, "C", 120, -6, 0.75, 0.8, "pathtosong"))
#    track_manager.add_track(Track("Track 2", "Artist 2", 240, "G", 140, -4, 0.85, 0.9, "pathtosong"))
#    print(track_manager.get_track_by_id("001"))
#    print(track_manager.get_track_by_id("002"))
#    collection_manager = CollectionManager()
#    collection_manager.add_collection(Collection("Album 1", "Album", "1, 2"))
#    collection_manager.add_collection(Collection("Compilation 1", "Compilation", "1, 2"))
#    collection_manager.add_collection(Collection("EP 1", "EP", ["001"], collection_manager.conn))
#    collection_manager.add_collection(Collection("Single 1", "Single", ["002"], collection_manager.conn))
#    collection_manager.add_collection(Collection("Playlist 1", "Playlist", ["001", "002"], collection_manager.conn))
#    collection_manager.add_collection(Collection("Main", "Main", [], collection_manager.conn))
#    collection1 = collection_manager.get_collection_by_id(1)
#    tracks = collection1.get_tracks(collection_manager.conn)
#    for track in tracks:
#        print(track)