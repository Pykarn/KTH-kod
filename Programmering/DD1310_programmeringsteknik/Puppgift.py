#Ian Knape Pyk, uppgift: 145, filnamn: Varuprisdatabas.py

#bestämma en global variabel som bestämmer vilken fil vi ska läsa från och skriva till
filnamn = "varudatabas.txt" 
#indata är filen som den ska läsa och returnerar en lista med obj
def läs_fil(filnamn):
    with open(filnamn, "r") as fil:
        lista = []
        for line in fil: 
            if ";" in line:
                for i in range(2):
                    lista.append(line.strip().split(";")[i])
            else:
                lista.append(line.strip())
        #Hur stor ska dellistorna av listan ska vara för att skapa en matris
        n=4
        #skapar matris som ska fyllas med dellistorna
        matris = []
        for i in range(0, len(lista), n):
            matris.append(lista[i:i + n])

        #gör om matrisen till en objekt lista
        obj_lista = []
        for i in range(len(matris)):            
            obj = Varodatabas(int(matris[i][0]),str(matris[i][1]),float(matris[i][2]),int(matris[i][3]))
            obj_lista.append(obj)
    return obj_lista

#bestämma största attributet för alla objekt, returnerar en int av längden på strängen
def största_sträng():
    obj_lista = läs_fil(filnamn)
    stränglista = []
    for obj in obj_lista:
        stränglista.append(str(obj.kod))
        stränglista.append(str(obj.namn))
        stränglista.append(f'{(obj.pris):.2f}')
    #returnerar längden av det största elementet i listan
    störst_längd = len(max(stränglista,key=len))
    
    return störst_längd
#definera en global variabel som lagrar utdatan från största sträng

#skapar en class databas
class Varodatabas:

    #skapa attribut för instanserna
    def __init__(self, kod, namn, pris, antal, antal_skannade=0):
        self.kod = kod
        self.namn = namn
        self.pris = pris
        self.antal = antal
        self.antal_skannade = antal_skannade
    

    #format för att skriva ut instanserna i kvittot
    def __str__(self):
        return f'{self.namn:<{största_sträng()+2}}{self.antal_skannade:<{största_sträng()+2}}{self.pris:<{största_sträng()+2}.2f}{self.pris*self.antal_skannade:.2f}'
    

    #textfil format för databasen
    def str_filformat(self):
        return f"{self.kod}\n{self.namn}\n{self.pris:.2f};{self.antal}\n"


    #metod för att uppdatera antalet av varor i databasen när man skannar, och returnerar en bool
    def uppdatera_antal(self, antal_varor):
        if self.antal >= antal_varor:
            self.antal -= antal_varor
            return True
        else:
            print(f"Fel: Det finns endast {self.antal} varor av {self.namn} kvar. Inmatning av {self.namn} kod: {self.kod} överskred antal varor som finns")
            print(f"Denna inmatning:", end= " ")
            return False


    #adderar parametern antal varor till antal skannade varor
    def uppdatera_antal_skannade(self, antal_varor):
        self.antal_skannade += antal_varor
#Slut på klassen

#returnera en matris med inputvärden beroende på vad man skriver i input
def mata_in_vara():
    matris = []
    kod_lista = []
    for obj in läs_fil(filnamn):
        kod_lista.append(obj.kod)
    
    #en While True sats som endast bryts om man skriver "#" och tillåter inputs av ett visst format
    while True: 
            varokod = input() 
            if varokod == "#":
                break

            #om kod-inputen är endast siffror antas antalet att vara 1
            elif(
            varokod.count(" ") == 0 and 
            varokod.isdigit() == True and
            int(varokod) in kod_lista
            ):
                dellista = [varokod, 1]          
                matris.append(dellista)
            
            #om det finns mellanslag antas antalet vara det som skrivs in efter
            elif varokod.count(" ") == 1:
                dellista = varokod.split(" ")

                #detta if-villkor tillåter endast digit inputs och kollar om kod-input matchar en varas kod
                if(
                dellista[0].isdigit() == True and 
                dellista[1].isdigit() == True and 
                int(dellista[0]) in kod_lista
                ):
                    matris.append(dellista)
                
                #detta elif-villkor tillåter negativa antal-inputs om man ångrar en tidigare input
                elif(   
                dellista[1][1:].isdigit() == True and 
                dellista[1][0] == "-" and
                int(dellista[0]) in kod_lista
                ):
                    matris.append(dellista)
                
                #om formatvillkoren inte uppfylls skrivs det ut ett felmeddelande
                else:
                    print("ogiltigt format, försök igen")
            else:
                print("ogiltigt format, försök igen")
    
    return matris


#indata är en lista av objekt och filnamn man skriver till i korrekt format
def skriv_till_fil(obj_lista, filnamn):
    with open(filnamn, "w") as fil:
        for obj in obj_lista:
            fil.write(obj.str_filformat())


#indata är en lista på vad man skannar skapar rätt format för utskriften av kvittot
def kvitto(skannade_obj_lista):
    total_antal = 0
    total_pris = 0

    #för varje objekt adderas deras pris och antalet till total antal och total pris
    for obj in skannade_obj_lista:
        total_antal += obj.antal_skannade
        total_pris += obj.pris * obj.antal_skannade
    #räknar ut hur långa sträcken ska vara beronde på total pris
    sträcklängd = 3*(största_sträng()+2)+len(f'{total_pris:.2f}')

    #skriver ut självaste kvittot med korrekt format
    print(f'{"Varunamn":<{största_sträng()+2}}{"Antal":<{största_sträng()+2}}{"A-pris":<{största_sträng()+2}}{"Summa"}')
    print(f"{'—'*sträcklängd}")
    for obj in skannade_obj_lista:
        print(obj)
    print(f"{'='*sträcklängd}")
    print(f'{"Total":<{största_sträng()+2}}{total_antal:<{2*(största_sträng()+2)}}{total_pris:.2f}')

 
#huvudprogrammet som skapar ett kvitto beroende på inmatning
def main():
    #skapar en objektlista från filen 
    obj_lista = läs_fil(filnamn)

    #skriver ut instruktioner för användare
    print ("Mata in varorna i detta format: [kod] [antal]↵ exempel: 100 3↵")
    print("Om du vill ändra antalet skannade varor innan kvittot skrivs ut kan man mata in negativa antal")
    print("För att skriva ut kvitto, skriv #.")
    #skapar tom lista för objekten som kommer att skannas
    skannade_obj_lista = []
    #anropar mata in vara funktionen och sparar utdatan i en variabel
    inmatningsmatris = mata_in_vara()

    #nästlad for loop som för varje rad i matrisen iterarar över alla objekt i objektlistan
    #itererar över varje rad i matrisen och definerar variablerna kod och antal varor som int()
    for lista in inmatningsmatris:
        kod = int(lista[0])
        antal_varor = int(lista[1])
        for obj in obj_lista:
            #kollar om objektet har samma kod som inmatningskoden
            if obj.kod == kod:
                #om det finns fler varor i databasen än antal blippade varor
                if obj.uppdatera_antal(antal_varor) == True:
                    #om man inte redan har skannat den varan
                    if obj not in skannade_obj_lista: 
                        obj.uppdatera_antal_skannade(antal_varor) 
                        #lägger till objektet i skannade objektlistan
                        skannade_obj_lista.append(obj)
                    #om man redan har skannat varan
                    else: 
                        #ändrar attributet antal skannade för objektet istället för att lägga till ett nytt objekt 
                        obj.uppdatera_antal_skannade(antal_varor)
                #om det inte finns fler varor i databasen än antal blippade varor
                else: 
                    print(f"({kod} {antal_varor}) räknades inte. Mata in eventuella ändringar:")
                    #skapar en ny inmatningsmatris som läggs till den gamla
                    ny_inmatningsmatris = mata_in_vara()
                    for lista in ny_inmatningsmatris:
                        inmatningsmatris.append(lista)
 
    #anropar kvitto-funktionen
    kvitto(skannade_obj_lista)
    
    #anropar skriv till fil-funktionen
    skriv_till_fil(obj_lista, filnamn)

#anropar huvudprogrammet
main()