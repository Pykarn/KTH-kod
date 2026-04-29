class Låt():
    def __init__(self,trackid,låtid,artistnamn,låttitel):
        self.trackid = trackid
        self.låtid = låtid
        self.artistnamn = artistnamn
        self.låttitel = låttitel

    def __str__(self):
        return f'{self.trackid} {self.låtid} {self.artistnamn} {self.låttitel}'

    def __lt__(self,other):
        return self.artistnamn < other.artistnamn