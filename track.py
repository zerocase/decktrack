class Track:
    def __init__(self, title, artist, duration, key, bpm, loudness, danceability, energy, quality,odir):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.key = key
        self.bpm = bpm
        self.loudness = loudness
        self.danceability = danceability
        self.energy = energy
        self.quality = quality
        self.odir = odir


    def __str__(self):
        return f"{self.title} - {self.artist} [{self.duration}s, key={self.key}, bpm={self.bpm}, loudness={self.loudness}, danceability={self.danceability}, energy={self.energy}, quality={self.quality}, odir={self.odir}"