class Track:
    def __init__(self, id, title, artist, duration, key, bpm, loudness, danceability, energy, ldir):
        self.id = id
        self.title = title
        self.artist = artist
        self.duration = duration
        self.key = key
        self.bpm = bpm
        self.loudness = loudness
        self.danceability = danceability
        self.energy = energy
        self.ldir

    def __str__(self):
        return f"{self.title} - {self.artist} [{self.duration}s, key={self.key}, bpm={self.bpm}, loudness={self.loudness}, danceability={self.danceability}, energy={self.energy}, ldir={self.ldir}"