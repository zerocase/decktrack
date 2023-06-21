import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from collection_manager import CollectionManager
from collection import Collection
from track_manager import TrackManager
from track import Track

track_manager = TrackManager()  
collection_manager = CollectionManager()
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


def prompter(playlist_link):
    source =""
    if "spotify" in playlist_link:
        source = "spotify"
        playlist = sp.playlist(playlist_link)
        #print(playlist)
        spotify_extractor(playlist, playlist_link)
    elif "deezer" in playlist_link:
        print("This feature is yet to be implemented")
    elif "music.youtube" in playlist_link:
        print("This feature is yet to be implemented")
    else:
        print("This does not seem to be a valid link!")




#def spotify_values(artistName, trackName):
#    artistrack = str(artistName)+ " " +str(trackName)
#    results = sp.search(artistrack, type="track")
#    items = results['tracks']['items']
#    if len(items) > 0:
#        track = items[0]
#        #print(sp.audio_features(track['id'])[0]) 
#        return track['id']
#    else:
#        return "No information on the Spotify database."


def spotify_extractor(playlist, remote_link):
    trackinfo = {
        "id" : "",
        "title" : "",
        "artist" : "",
        "duration" : 0,
        "key" : 0,
        "bpm" : 0,
        "loudness" : 0,
        "danceability" : 0,
        "energy" : 0,
    }
    allinfo = []
    for item in playlist['tracks']['items']:
        trackinfo["id"] = item['track']['id']
        trackinfo["title"] = item['track']['name']
        for artist in item['track']['artists']:
            trackinfo['artist'] = artist['name']
        summary = sp.audio_features(trackinfo["id"])[0]
        trackinfo["duration"] = summary['duration_ms'] /1000
        trackinfo["key"] = summary['key']
        trackinfo["bpm"] = summary['tempo']
        trackinfo["loudness"] = summary['loudness']
        trackinfo["danceability"] = summary['danceability']
        trackinfo["energy"] = summary['energy']
        allinfo.append(trackinfo.copy())
    spotify_importer(allinfo, playlist['name'], remote_link)

def spotify_importer(allinfo, name, remote_link):
    default_collection_type = "Playlist"
    collection_name = name
    lst = collection_manager.get_collections_starting_with(collection_name)
    max_val = 0
    for collection in lst:
        # .* - (\d+)
        result = re.match(f".* - (\d+)", collection[0])
        if result:
            max_val = max(max_val, int(result.group(1)))
    if len(lst)>0:
        collection_name = f"{collection_name} - {max_val+1}"
        
    spotify_collection = Collection(collection_name, default_collection_type)
    collection_manager.add_collection(spotify_collection)
    for track in allinfo:
        print(track)
        track_inf = Track(str(track['title']), str(track['artist']), float(track['duration']), str(track['key'] ), float(track['bpm']), float(track['loudness']), float(track['danceability']), float(track['energy']), None, remote_link)
        track_manager.add_track(track_inf)
        collection_manager.add_track_to_collection(spotify_collection, track_inf)


#prompter("https://open.spotify.com/playlist/3c9cD2tAG2jRyk5QNWxyJH?si=ffb9469e7b934a8d")