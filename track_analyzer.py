import librosa

antrack = "E://ProjectDevelop//decktrack//data//testracks//Neurokontrol_Emile.flac"



def analyze_track(audio_file_path):
    y, sr = librosa.load(audio_file_path)

    # Compute key

    # Compute BPM
    bpm, beats = librosa.beat.beat_track(y=y, sr=sr)

    # Compute loudness
    loudness = librosa.core.amplitude_to_db(librosa.feature.rms(y=y), ref=0.01)
    # Compute danceability
    # Compute energy

    print(loudness)
    print(bpm)


analyze_track(antrack)