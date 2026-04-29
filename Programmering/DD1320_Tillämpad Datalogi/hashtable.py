class HashNode:
    #Noder till klassen Hashtable
    def __init__(self, key="", data=None):
        self.key = key
        self.data = data


class Hashtable:
    #Hashtabell med linjär probning

    def __init__(self, size):
        #size: hashtabellens storlek
        self.size = size
        self.table = [None] * size  # tom tabell

    def store(self, key, data):
        #Lagrar 'data' med nyckeln 'key' i tabellen
        index = self.hashfunction(key)
        start_index = index  # för att upptäcka om vi gått runt

        while True:
            node = self.table[index]
            if node is None or node.key == key:
                # tom plats eller samma nyckel → lagra/uppdatera
                self.table[index] = HashNode(key, data)
                return
            # annars: krock → prova nästa
            index = (index + 1) % self.size
            if index == start_index:
                # tabellen är full
                raise MemoryError("Hashtable full")
            
    def search(self, key):
        #Hämtar data för 'key'
        #KeyError om ej hittad
        index = self.hashfunction(key)
        start_index = index

        while True:
            node = self.table[index]
            if node is None:
                raise KeyError(key)
            if node.key == key:
                return node.data
            index = (index + 1) % self.size
            if index == start_index:
                raise KeyError(key)
            
    def hashfunction(self, key):
        #beräknar hashfunktionen för key
        h = 0
        for c in key:
            h = (h * 32 + ord(c)) % self.size
        return h