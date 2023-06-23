import os
import re
import music_tag
from collection_manager import CollectionManager
from collection import Collection
from track_manager import TrackManager
from track import Track
from track_analyzer import TrackAnalysis
from gui_relay import InfoPane
import SongNameSplit

track_manager = TrackManager()  
collection_manager = CollectionManager()



class CollectionCreator:
    def get_all_folders(self, input_dir):
        paths_all = []
        collection_paths =[]
        if not os.path.exists(input_dir):
            raise FileNotFoundError("Could not find path: %s"%(input_dir))
        for dirpath, dirnames, filenames in os.walk(input_dir):
            paths_all.append(dirpath)
        for path in paths_all:
            if any(File.endswith(".flac") or File.endswith(".wav") or File.endswith(".mp3") for File in os.listdir(path)):
                collection_paths.append(path)
        #print(collection_paths)
        return collection_paths


    def collection_from_folder(self, loc, analyze):
        default_collection_type = "Playlist"
        collection_name = os.path.basename(loc)
        # Fetch from the DB all the collections beginning with collection_name
        lst = collection_manager.get_collections_starting_with(collection_name)
        max_val = 0
        for collection in lst:
            # .* - (\d+)
            result = re.match(f".* - (\d+)", collection[0])
            if result:
                max_val = max(max_val, int(result.group(1)))
        if len(lst)>0:
            collection_name = f"{collection_name} - {max_val+1}"
        
        folder_collection = Collection(collection_name, default_collection_type)
        collection_manager.add_collection(folder_collection)

        for file in os.listdir(loc):
            if file.endswith(".flac") or file.endswith(".wav") or file.endswith(".mp3"):
                track_data = music_tag.load_file(os.path.join(loc,file))
                if not track_data['title']:
                    try:
                        title = os.path.splitext("".join(file.split(" - ")[1:]))[0]
                        track_data['title'] = title
                    except:
                        track_data['title'] = file
                if not track_data['artist']:
                    try:
                        artist = file.split(" - ")[0]
                        track_data['artist'] = artist
                    except:
                        track_data['artist'] = 'Unknown'
                if analyze == True:
                    analysis_data = TrackAnalysis.analyze_track(os.path.join(loc,file))
                    track = Track(str(track_data['title']), str(track_data['artist']), float(analysis_data[0]), str(analysis_data[1]), float(analysis_data[2]), float(analysis_data[3]), float(analysis_data[4]), float(analysis_data[5]), int(track_data['#bitrate'])/1000, os.path.join(loc,file))
                else:
                    #print(track_data)
                    track = Track(str(track_data['title']), str(track_data['artist']),None, None, None, None, None, None, int(track_data['#bitrate'])/1000, os.path.join(loc,file))                    
                track_manager.add_track(track)
                collection_manager.add_track_to_collection(folder_collection, track)
            #else:
            #    raise ValueError("Could not find any audio files in the folder: %s"%(loc))

    
    def analyze_tracks(self, tracks_info, collection_name):
        numtracks = len(tracks_info)
        track_num = 0
        for track in tracks_info:
            track_num +=1
            track_data = track_manager.get_track_by_title_artist(track[0], track[1])
            currinfo = f"Analyzing... ({track_num}/{numtracks}) | Collection: {collection_name} | Track: {track[0]}"
            InfoPane.refresh_info_pane(currinfo)
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
        
    
