import os
import music_tag
from collection_manager import CollectionManager
from collection import Collection
from track_manager import TrackManager
from track import Track
from track_analyzer import TrackAnalysis

class CollectionCreator:

    def collection_from_folder(self, loc, analyze):
        track_manager = TrackManager()
        collection_manager = CollectionManager()
        default_collection_type = "Playlist"
        collection_name = os.path.basename(loc)
        folder_collection = Collection(collection_name, default_collection_type)
        collection_manager.add_collection(folder_collection)    

        for file in os.listdir(loc):
            if file.endswith(".flac") or file.endswith(".wav") or file.endswith(".mp3"):
                track_data = music_tag.load_file(os.path.join(loc,file))
                if analyze == True:
                    analysis_data = TrackAnalysis.analyze_track(os.path.join(loc,file))
                    track = Track(str(track_data['title']), str(track_data['artist']), float(analysis_data[0]), str(analysis_data[1]), float(analysis_data[2]), float(analysis_data[3]), float(analysis_data[4]), float(analysis_data[5]), int(track_data['#bitrate'])/1000, os.path.join(loc,file))
                else:
                    #print(track_data)
                    track = Track(str(track_data['title']), str(track_data['artist']),None, None, None, None, None, None, int(track_data['#bitrate'])/1000, os.path.join(loc,file))                    
                track_manager.add_track(track)
                collection_manager.add_track_to_collection(folder_collection, track)
    
    def analyze_tracks(self, collection):
        track_manager = TrackManager()
        collection_manager = CollectionManager()
        collection_name = collection

        for track in collection_manager.get_tracks_from_collection(collection):
            track_data = music_tag.load_file(track.get_odir())
            analysis_data = TrackAnalysis.analyze_track(track.get_odir())
            track = Track(str(track_data['title']), str(track_data['artist']), float(track_data['length']), str(analysis_data[1]), float(analysis_data[2]), float(analysis_data[3]), float(analysis_data[4]), float(analysis_data[5]), int(track_data['#bitrate'])/1000, track.get_odir())
            track_manager.update_track(track)
        
    
