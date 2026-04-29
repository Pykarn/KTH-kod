from hashtable import Hashtable
import csv

class Drama:
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
        return f"{self.Drama_Name} ({self.Year})"

def läs_in_kdrama(filnamn, size):
    """Läser in drama-objekt från CSV och lägger in dem i en Hashtable"""
    hashtabell = Hashtable(size)
    with open(filnamn, mode="r", encoding="utf-8") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=",")
        next(file_reader)  # hoppa över rubriker

        for row in file_reader:
            if len(row) >= 10:
                drama = Drama(*row[:10])
                hashtabell.store(drama.Drama_Name, drama)
    return hashtabell

def testa():
    # Skapa en lagom stor tabell (t.ex. 50 om filen har ~30 draman)
    kdrama = läs_in_kdrama("kdrama.csv", 500)

    # Testa sökningar
    test1 = "Ian"
    test2 = "Legend of the Blue Sea"
    test3 = "The forbidden marriage"

    for namn in [test1, test2, test3]:
        try:
            print(kdrama.search(namn))
        except KeyError:
            print(f"Nyckeln '{namn}' finns inte i hashtabellen.")



if __name__ == "__main__":
    testa()

