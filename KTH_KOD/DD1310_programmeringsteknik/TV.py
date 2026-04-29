class TV:
    def __init__(self, name, max_channel, current_channel, max_volume, current_volume): #skapar objektet med dessa attribut namn, max kanal osv
        self.name = name
        self.max_channel = max_channel
        self.current_channel = current_channel
        self.max_volume = max_volume
        self.current_volume = current_volume

    #returnerar namn, nuvarande kanal, nuvarande ljudnivå
    def __str__(self): 
        return f"\n{self.name}\nKanal: {self.current_channel}\nLjudnivå: {self.current_volume}"
    #returnerar en sträng med namn på TV:n, högsta möjliga kanal, inställd kanal, högsta möjliga ljudnivå & inställd ljudnivå
    def str_for_file(self):

        return f"{self.name},{self.max_channel},{self.current_channel},{self.max_volume},{self.current_volume}" 

    def change_channel(self, new_channel): #ändrar kanal och returnerar true om kanalen är mellan 0 och max kanal annars returner False
        if 0<new_channel<=self.max_channel:
            self.current_channel = new_channel
            return True
        else: 
            return False
    #ökar ljudnivån med 1 om if villkoret är uppfyllt
    def increase_volume(self): 
        if self.current_volume<self.max_volume: 
            self.current_volume+=1
            return True
        else:
            return False
    #sänker ljudnivån med 1 om if villkoret är uppfyllt
    def decrease_volume(self): 
        if self.current_volume>0:
            self.current_volume-=1
            return True
        else:
            return False