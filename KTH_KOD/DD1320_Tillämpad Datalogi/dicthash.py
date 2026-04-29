class DictHash:
    def __init__(self):
        #skapar dictionary
        self.dictionary = {}

    def store(self, nyckel, data):
        #lagrar data i dictionary med nyckel som key
        self.dictionary[nyckel] = data

    def search(self, nyckel):
        #slår upp nyckel i dictionary och returnerar värdet
        if nyckel in self.dictionary:
            return self.dictionary[nyckel]
        else:
            raise KeyError
    def __getitem__(self, nyckel):
        #möjligt att skriva d[nyckel] istället för d.search(nyckel)
        return self.search(nyckel)

    def __contains__(self, nyckel):
        #möjligt att skriva 'if nyckel in d'
        return nyckel in self.dictionary
