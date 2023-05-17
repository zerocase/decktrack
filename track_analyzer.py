import librosa
import numpy as np

class TrackAnalysis:
    def krumhansl_schmuckler(y, sr):
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        # Calculate key profiles
        key_profiles = np.zeros((12, chroma.shape[1]))
        for i in range(12):
            chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr, C=None, hop_length=512, fmin=None, n_chroma=12,
                                                    bins_per_octave=36, tuning=i, norm=2, threshold=None,
                                                    window=None)
            key_profiles[i] = np.sum(chroma * chroma_cqt, axis=0)

        # Apply Krumhansl-Schmuckler weighting
        weights = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        weighted_profiles = key_profiles * weights[:, np.newaxis]

        # Find key with highest correlation
        correlations = np.zeros(12)
        for i in range(12):
            correlations[i] = np.corrcoef(weighted_profiles[i], np.sum(weighted_profiles, axis=0))[0, 1]
        key = np.argmax(correlations)

        # Convert key index to key name
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_name = key_names[key]

        return key_name

    def dfa(y, minTau=10, maxTau=100):
        # Convert audio to mono if it is stereo
        if y.ndim > 1:
            y = librosa.core.to_mono(y)
    
        # Calculate the cumulative sum of the audio signal
        cumsum = np.cumsum(y - np.mean(y))
    
        # Calculate the range of tau values
        tau = 2 ** np.arange(np.floor(np.log2(minTau)), np.ceil(np.log2(maxTau)))
    
        # Calculate the fluctuation for each tau value
        fluctuation = np.zeros(len(tau))
        for i, t in enumerate(tau):
            segments = np.reshape(cumsum[:int(t * (len(cumsum) // t))], (-1, int(t)))
            local_trend = np.mean(segments, axis=1, keepdims=True)
            segments -= local_trend
            fluctuation[i] = np.sqrt(np.mean(segments ** 2))
    
        # Fit a line to the log-log plot of tau vs fluctuation
        poly = np.polyfit(np.log2(tau), np.log2(fluctuation), 1)
    
        # Return the DFA exponent as a measure of danceability
        return poly[0]




    def analyze_track(audio_file_path):
        # Load Track on Mono
        y, sr = librosa.load(audio_file_path)

        # Compute BPM
        bpm, beats = librosa.beat.beat_track(y=y, sr=sr, units='time', trim=False, hop_length=256)

        # Compute energy rms
        energy = librosa.feature.rms(y=y)

        # Compute Key
        key = TrackAnalysis.krumhansl_schmuckler(y, sr)

        # Compute Loudness
        loudness = librosa.core.power_to_db(energy, ref=1.0, amin=1e-20, top_db=None)

        # Compute Duration
        duration = librosa.get_duration(y=y, sr=sr)

        # Compute Danceability
        danceability = TrackAnalysis.dfa(y)

        analysis_data = [round(duration, 2), key, round(bpm, 2), round(loudness.mean(), 2), danceability, round(energy.mean(), 2)]

        return analysis_data

#tdir = "E://MusicLibrary//Nicotine//Kurnugû - Third Foundation//[NONE] Ikiryō - At Dawn (2021)//01. Ikiryō - At Dawn.flac"
#print(TrackAnalysis.analyze_track(tdir))
