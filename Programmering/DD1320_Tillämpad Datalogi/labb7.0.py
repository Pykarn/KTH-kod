from dicthash import DictHash
from hashtable import Hashtable
import csv

class Drama():

    def __init__(self, Drama_Name, Rating, Actors, Viewship_Rate, Genre, Director, Writer, Year, No_of_Episodes, Network):
        self.Drama_Name = Drama_Name
        self.Rating = float(Rating)
        self.Actors = Actors
        self.Viewship_Rate = float(Viewship_Rate)
        self.Genre = Genre
        self.Director = Director
        self.Writer = Writer
        self.Year = int(Year)
        self.No_of_Episodes = int(No_of_Episodes)
        self.Network = Network


    def __str__(self):
        return f'{self.Drama_Name}({self.Year})'
    
def läs_in_kdrama(filnamn):
    #Läser in dramaobjekt från CSV och lagrar dem i en DictHash
    hashtabell = DictHash()
    with open(filnamn, mode='r', encoding='utf-8') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        next(file_reader)  # hoppa över rubrikraden

        for row in file_reader:
            # Skapa Drama-objekt (radens 10 kolumner)
            if len(row) >= 10:
                drama = Drama(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                # Använd drama-titeln som nyckel
                hashtabell.store(row[0], drama)
    return hashtabell
   
def testa():
    kdrama = läs_in_kdrama("kdrama.csv")
    test1 = "Ian"
    test2 = "Legend of the Blue Sea"
    test3 = "The forbidden marriage"
    try:
        print(kdrama[test1])
    except KeyError:
        print(f"nyckeln {test1} finns inte")
    try:
        print(kdrama[test2])
    except KeyError:
        print(f"nyckeln {test2} finns inte")
    try:
        print(kdrama[test3])
    except KeyError:
        print(f"nyckeln {test3} finns inte")

def main():
    hashtable = None
    
    while True:
        line = input()
        key, *value = line.split()
        if key == '#':
            print('#')
            break
        elif key == 'init' and len(value) > 0:
            size = int(value[0])
            hashtable = Hashtable(size)
            print('New size:', size)
        elif len(value) > 0:
            hashtable.store(key, value[0])
            print(key, '<-', value[0])
        else:
            try:
                value = hashtable.search(key)
                print(f'{key}: {value}')
            except KeyError:
                print('KeyError:', key)


if __name__ == "__main__":
    testa()


"""
Varför hashning är snabb:
den beräknar direkt indexet i tabellen i stället för att jämföra många element

Hur krockar hanteras:
med linjär probning (går till nästa lediga plats)

Varför hashfunktionen fungerar bra:
sprider nycklar över hela tabellen (multiplikation med 32 och modulus)

Varför tabellen inte får vara full:
annars fastnar probningen i evig loop
"""
