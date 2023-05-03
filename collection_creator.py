import os
import music_tag
from collection_manager import CollectionManager
from collection import Collection
from track_manager import TrackManager
from track import Track

def collection_from_folder(loc):
    track_manager = TrackManager()
    collection_manager = CollectionManager()
    default_collection_type = "Playlist"
    collection_name = os.path.basename(loc)
    folder_collection = Collection(collection_name, default_collection_type)
    collection_manager.add_collection(folder_collection)    

    for file in os.listdir(loc):
        if file.endswith(".flac") or file.endswith(".wav") or file.endswith(".mp3"):
            track_data = music_tag.load_file(os.path.join(loc,file))
            track = Track(str(track_data['title']), str(track_data['artist']), 180, "C", 120, -6, 0.75, 0.8, os.path.join(loc,file))
            track_manager.add_track(track)
            collection_manager.add_track_to_collection(folder_collection, track)



collection_from_folder("E://ProjectDevelop//decktrack//data//testracks")