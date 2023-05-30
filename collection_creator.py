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
    
    def analyze_tracks(self, tracks_info):
        track_manager = TrackManager()
        collection_manager = CollectionManager()
        #print(tracks_info)
        for track in tracks_info:
            track_data = track_manager.get_track_by_title_artist(track[0], track[1])   
            #print(track_data)
            #print(track_data[0])
            analysis_data = TrackAnalysis.analyze_track(track_data[10])
            track_object = Track(track_data[1], track_data[2], float(analysis_data[0]), str(analysis_data[1]), float(analysis_data[2]), float(analysis_data[3]), float(analysis_data[4]), float(analysis_data[5]), int(track_data[9]), track_data[10])
            track_manager.update_track(track_object, track_data[0])

        #for track in tracks:
        #    track_data = music_tag.load_file(os.path.join(loc,file))
        #    track = track_manager.get_track_by_title_artist(track.title, track.artist)
        #    track = Track(str(track_data['title']), str(track_data['artist']), float(track_data['length']), str(analysis_data[1]), float(analysis_data[2]), float(analysis_data[3]), float(analysis_data[4]), float(analysis_data[5]), int(track_data['#bitrate'])/1000, track_manager.get_odir(track))
        #    track_manager.update_track(track)
        
    
