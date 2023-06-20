from track_manager import TrackManager
from collection_manager import CollectionManager
from collection_creator import CollectionCreator
from track import Track
from collection import Collection
import db
import time


if __name__ == '__main__':
    #start_time = time.time()
    if not db.check_db_exists():
        db.initialize_tables()
    import gui
    #track_manager = TrackManager()  
    #collection_manager = CollectionManager()
    #collection_creator = CollectionCreator()
    #dir1 = "E://MusicLibrary//Nicotine//Kurnugû - Third Foundation//[NONE] Bereneces - Chambers (2021)"
    #collection_creator.collection_from_folder(dir1, True)
    #print("--- %s seconds ---" % (time.time() - start_time))
#    print(collection_manager.get_collections())
    #tr1 = Track("Track 1", "Artist 1", 180, "C", 120, -6, 0.75, 0.8, "pathtosong")
   # tr2 = Track("Track 2", "Artist 2", 240, "G", 140, -4, 0.85, 0.9, "pathtosong")
   # track_manager.add_track(tr1)
    #track_manager.add_track(tr2)
#    print(track_manager.get_track_by_id("001"))
#    print(track_manager.get_track_by_id("002"))
#
    #coll1 = Collection("Compilation 1", "Compilation")


    #collection_manager.add_collection(coll1)
    #collection_manager.add_track_to_collection(coll1, tr1)
    #collection_manager.add_track_to_collection(coll1, tr2)


    
#    collection_manager.add_collection(Collection("EP 1", "EP", ["001"], collection_manager.conn))
#    collection_manager.add_collection(Collection("Single 1", "Single", ["002"], collection_manager.conn))
#    collection_manager.add_collection(Collection("Playlist 1", "Playlist", ["001", "002"], collection_manager.conn))
#    collection_manager.add_collection(Collection("Main", "Main", [], collection_manager.conn))
#    collection1 = collection_manager.get_collection_by_id(1)
#    tracks = collection1.get_tracks(collection_manager.conn)
#    for track in tracks:
#        print(track)