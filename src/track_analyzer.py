import librosa
import numpy as np

class TrackAnalysis:
    def krumhansl_schmuckler(waveform, sr):
        waveform = waveform
        sr = sr
        tstart=22
        tend = 33
        
        tstart = librosa.time_to_samples(tstart, sr=sr)
        tend = librosa.time_to_samples(tend, sr=sr)
        # Calculate key profiles
        y_segment = waveform[tstart:tend]
        chromograph = librosa.feature.chroma_cqt(y=y_segment, sr=sr, bins_per_octave=24)
        # chroma_vals is the amount of each pitch class present in this time interval
        chroma_vals = []
        for i in range(12):
            chroma_vals.append(np.sum(chromograph[i]))
        pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        # dictionary relating pitch names to the associated intensity in the song
        keyfreqs = {pitches[i]: chroma_vals[i] for i in range(12)} 
        
        keys = [pitches[i] + ' major' for i in range(12)] + [pitches[i] + ' minor' for i in range(12)]

        # use of the Krumhansl-Schmuckler key-finding algorithm, which compares the chroma
        # data above to typical profiles of major and minor keys:
        maj_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        min_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

        # finds correlations between the amount of each pitch class in the time interval and the above profiles,
        # starting on each of the 12 pitches. then creates dict of the musical keys (major/minor) to the correlation
        min_key_corrs = []
        maj_key_corrs = []
        for i in range(12):
            key_test = [keyfreqs.get(pitches[(i + m)%12]) for m in range(12)]
            # correlation coefficients (strengths of correlation for each key)
            maj_key_corrs.append(round(np.corrcoef(maj_profile, key_test)[1,0], 3))
            min_key_corrs.append(round(np.corrcoef(min_profile, key_test)[1,0], 3))

        # names of all major and minor keys
        key_dict = {**{keys[i]: maj_key_corrs[i] for i in range(12)}, 
                         **{keys[i+12]: min_key_corrs[i] for i in range(12)}}
        
        # this attribute represents the key determined by the algorithm
        key = max(key_dict, key=key_dict.get)
        bestcorr = max(key_dict.values())
        #print(key)
        return key
    
    
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
