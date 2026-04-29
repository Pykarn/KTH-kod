import csv
def readfile():
    with open('kdrama.csv', mode = 'r') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            print(row)



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

    def __lt__(self, other):
        return self.Drama_Name < other.Drama_Name

    def return_genre(self):
        return self.Genre
    
    def after_2020(self):
        if self.Year > 2020:
            print("Efter 2020")
        else:
            print("år 2020 eller tidigare")

def create_2_objects():
    with open('kdrama.csv', mode = 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        obj_list = []
        next(reader)
        i = 0
        for rad in reader:
            if i < 2:
                objekt = Drama(rad[0],rad[1],rad[2],rad[3],rad[4],rad[5],rad[6],rad[7],rad[8],rad[9])
                obj_list.append(objekt)
                i+=1
            else:
                break
    
    obj_list.sort()
    print(obj_list[0])
    print(obj_list[0].return_genre())
    obj_list[0].after_2020()
    print(obj_list[1])
    print(obj_list[1].return_genre())
    obj_list[1].after_2020()


def create_object_list():
    with open('kdrama.csv', mode = 'r') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        i=0
        obj_list = []
        for row in file_reader:
            if i>0:
                obj = Drama(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
                obj_list.append(obj)
            else:
                i+=1
                continue
    return obj_list


def search(lista):
    search_name = input("Sök efter Dramanamn: ").strip().lower()  
    found = False
    for drama in lista:
        if drama.Drama_Name.strip().lower()==search_name: 
            print(drama)
            found = True 
            break
    if found == False:
        print("inget drama hittades")
       

#test  
obj_lista = create_object_list()

#create_2_objects()

#sorterad = sorted(obj_lista)
#for item in sorterad:
    #print(item)
    #item.return_genre()
    #item.after_2020()

search(obj_lista)


