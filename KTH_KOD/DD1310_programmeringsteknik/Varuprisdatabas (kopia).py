# Karl Bengtsson, uppgift 145

#De enda globala variablerna vilka står för köpets totala kostnad (summa) samt hur många varor som skannats
summa = 0
totalt_antal = 0

#Klass som skapar ett objekt i form av en vara med attributen:
#  varans kod, varans namn, varans artikelpris, varans lagerstatus, antal varor som angivits i köpet och varans summakostnad
class Vara: 

    def __init__(self, kod, namn, artikelpris, lagerstatus, antal_skannade = 0):
        self.kod = kod
        self.namn = namn
        self.artikelpris = artikelpris
        self.lagerstatus = lagerstatus
        self.antal_skannade = antal_skannade
        self.tot_kostnad = antal_skannade*artikelpris
    
    #Ger en utskrift på varans kvittoattribut, dvs det som ska visas på kvittot, baserat på varje kolumns bredd
    def str_för_kvitto(self,kolumnbredd1,kolumnbredd2,kolumnbredd3,kolumnbredd4):
        return f"{self.namn:<{kolumnbredd1}}{self.antal_skannade:<{kolumnbredd2}}{self.artikelpris:>{kolumnbredd3}.2f}{self.tot_kostnad:>{kolumnbredd4}.2f}"

    #Anpassad för att skriva över till vald fil
    def str_för_fil(self):
        return f"{self.kod}\n{self.namn}\n{self.artikelpris:.2f};{self.lagerstatus}\n"
    
    #Om villkoren uppfylls ändrar funktionen varans lagerstatus, totala kostnad och antal skannade
    def redigera_vara(self, antal_skannade):
        if self.lagerstatus-antal_skannade >= 0 and self.antal_skannade + antal_skannade >= 0:
            self.lagerstatus = self.lagerstatus - antal_skannade
            self.antal_skannade = self.antal_skannade + antal_skannade
            self.tot_kostnad = self.artikelpris*self.antal_skannade
            global summa
            global totalt_antal
            summa += self.tot_kostnad
            totalt_antal += antal_skannade
            return True
        else: 
            return False
    
    #Nollställer en varas attribut så att lagerstatus är oförändrad och antal skannade = 0
    def nollställ_vara(self):
        self.lagerstatus = self.lagerstatus + self.antal_skannade
        global totalt_antal
        global summa
        totalt_antal -= self.antal_skannade
        summa -= self.tot_kostnad
        self.antal_skannade = 0

#Läser från vald fil och skapar objekt (varor) utfrån datan. Returnerar en lista med varorna som finns i databasen
def läs_från_fil(filnamn):
    objektslista = []
    fil = open(filnamn, "r")
    kod = fil.readline().strip()
    while kod != "":
        namn = fil.readline().strip()
        #Skapar en lista med två element på varans pris och antal i lager
        artikelpris_lagerstatus_lista = (fil.readline().strip().split(";"))
        objekt = Vara(int(kod), namn, float(artikelpris_lagerstatus_lista[0]), int(artikelpris_lagerstatus_lista[1]))
        objektslista.append(objekt)
        kod = fil.readline().strip()
    fil.close()
    return objektslista

#Skriver över objektens nuvarande data till vald fil
def skriv_till_fil(objektslista,filnamn):
    fil = open(filnamn, "w")
    for vara in objektslista:
        fil.write(vara.str_för_fil())

#Tar emot objektslistan från läs_från_fil och returnerar en lista med objektens (varornas) koder 
def skapa_lista_alla_koder(objektslista):
    lista_alla_koder = []
    for vara in objektslista:
        lista_alla_koder.append(vara.kod)
    return lista_alla_koder
    
#Returnerar giltig inmatning, i form av en lista, till kontrollera_vara
def skanna_varor():
    inmatning = input()
    while inmatning != "#":
        #Gör om värdena till en lista
        lista_inmatning = inmatning.split()
        #Vid inmatnig av endast kod, då tolkar systemet det som blipp av en vara
        if len(lista_inmatning) == 1: 
            try:
                kod = int(lista_inmatning[0])
                return [kod,1]
                
            except ValueError:
                print("Fel inmatning, vänligen försök igen: ")
                inmatning = input()
        #Om inmatningen anger hur många varor som skannats
        elif len(lista_inmatning) == 2: 
            try:
                if lista_inmatning[1] == "-":
                    kod = int(lista_inmatning[0])
                    return [kod, "-"]
                else:
                    kod = int(lista_inmatning[0])
                    antal = int(lista_inmatning[1])
                    return [kod, antal]
            except ValueError:
                print("Fel inmatning, ange endast heltal: ")
                inmatning = input()
        else:
            print("Fel inmatning, vänligen försök igen: ")
            inmatning = input()
    #Returnerar här # om det matades in i inputen. 
    return inmatning

#Säkerställer att den skannade varan finns i systemet
def kontrollera_vara(inmatning, lista_alla_koder):
    kod = inmatning[0]
    if kod in lista_alla_koder:
        return True
    else:
        print("Varan finns inte i systemet, vänligen försök igen:") 
        return False

#Ändrar objektens attribut efter att kontrollera_vara säkerställt kodens existens i databasen
def registrera_skannad_vara(lista_inmatning, lista_alla_koder, lista_skannade_koder, objektslista):
    antal_skannade = lista_inmatning[1]
    varukod = lista_inmatning[0]
    #Varukod har samma index i lista_alla_koder som motsvarande objekt i objektslistan på varor - tilldelar skannad_vara rätt objekt.
    skannad_vara = objektslista[lista_alla_koder.index(varukod)]
    #Om koden inte finns i systemet men man ändå väljer att nollställa varan så händer ingenting
    if antal_skannade == "-" and varukod not in lista_skannade_koder:
        return lista_skannade_koder
    elif antal_skannade == "-" and varukod in lista_skannade_koder:
        skannad_vara.nollställ_vara()
        lista_skannade_koder.remove(varukod)
        return lista_skannade_koder
    elif antal_skannade < 0 and skannad_vara.antal_skannade == 0:
        print(f"Vara med kod {skannad_vara.kod} ingår inte i ditt köp, vänligen fortsätt inmatning: ")
        return lista_skannade_koder
    elif antal_skannade == 0:
        return lista_skannade_koder
    else:
        registrering = skannad_vara.redigera_vara(antal_skannade)
        if varukod not in lista_skannade_koder and registrering == True:
            lista_skannade_koder.append(varukod)
            uppdateradlista = lista_skannade_koder
            return uppdateradlista
        elif varukod in lista_skannade_koder and registrering == True:
            if skannad_vara.antal_skannade == 0:
                lista_skannade_koder.remove(varukod)
                return lista_skannade_koder
            else:
                return lista_skannade_koder
        elif skannad_vara.antal_skannade + antal_skannade < 0:
            print("Du kan inte plocka bort fler varor än du skannat, vänligen försök igen:")
            return lista_skannade_koder
        else: 
            print(f"Kunde inte skanna vara med kod {skannad_vara.kod} ({skannad_vara.lagerstatus} kvar i lager), vänligen försök igen:")
            return lista_skannade_koder

#Denna funktion sorterar ut den längsta strängen för varje av de fyra kolumnerna på kvittot,
# på så vis får man en estetiskt fulländad formatering och minimal kvittoåtgång.
def bestäm_längsta_strängar(objektslista_skannade):
    global totalt_antal
    global summa
    #Stränglistans originalvärden är referensvärden som alltid visas på kvittot, 
    # alltså de längsta strängarna om ingen längre sträng förekommer
    stränglista = ["Antal", "Summa","Varunamn","A-pris"]
    for vara in objektslista_skannade: 
        stränglista.append(str(vara.namn))
        stränglista.append(str(f"{vara.artikelpris:.2f}"))
    str_totalt_antal = str(totalt_antal)
    str_summa = str(f"{summa:.2f}")
    stränglista2 = []
    stränglista2.append(str_totalt_antal)
    stränglista2.append(str_summa)
    lista_längsta_strängar = []
    #Sorterar ut längsta varunamn och längsta artikepris
    for i in range(2,4):
        längst_sträng = stränglista[i]
        #for-satsen itererar över vartannat element eftersom varunamnens och artikelprisens ordning är sådan i stränglistan
        for sträng in (stränglista[i+2:len(stränglista):2]):
            if len(sträng) > len(längst_sträng):
                längst_sträng = sträng
        lista_längsta_strängar.append(längst_sträng)
    #Sorterar ut längsta summa och längsta antal
    for j in range(2):
        längst_sträng = stränglista[j]
        if len(stränglista2[j]) > len(längst_sträng):
            längst_sträng = stränglista2[j]
        lista_längsta_strängar.append(längst_sträng)
    return lista_längsta_strängar

#Returnerar en lista på de objekt som skannats med hjälp av listan på skannade koder
def uppdatera_objektslista(objektslista, lista_skannade_koder, lista_alla_koder):
    lista_skannade_varor = []
    for varukod in lista_skannade_koder:
        #Varukoden har samma index i lista_alla_koder som motsvarande objekt i objektslistan
        skannad_vara = objektslista[lista_alla_koder.index(varukod)]
        lista_skannade_varor.append(skannad_vara)
    return lista_skannade_varor

#Skriver ut kvittot formaterat via den längsta srängen för varje kolumn
def skriv_kvitto(lista_skannade_varor,lista_längsta_strängar):
    global summa
    global totalt_antal
    kolumnbredd1 = len(lista_längsta_strängar[0])+3 #Längst sträng i kolumnen "Varunamn" + ytterligare tre tecken
    kolumnbredd2 = len(lista_längsta_strängar[2]) #Längst sträng i kolumnen "Antal"
    kolumnbredd3 = len(lista_längsta_strängar[1])+3 #Längst sträng i kolumnen "A-pris" + ytterligare tre tecken
    kolumnbredd4 = len(lista_längsta_strängar[3])+3 #Längst sträng i kolumnen "Summa" + ytterligare tre tecken
    kolumnbredd_tot = kolumnbredd1+kolumnbredd2+kolumnbredd3+kolumnbredd4
    print(f"{'Varunamn':<{kolumnbredd1}}{'Antal':<{kolumnbredd2}}{'A-pris':>{kolumnbredd3}}{'Summa':>{kolumnbredd4}}")
    print("-"*kolumnbredd_tot)
    for vara in lista_skannade_varor:
        print(vara.str_för_kvitto(kolumnbredd1,kolumnbredd2,kolumnbredd3,kolumnbredd4))
    print("="*kolumnbredd_tot)
    print(f"{'Total':<{kolumnbredd1}}{totalt_antal:<{kolumnbredd2}}{summa:>{kolumnbredd3+kolumnbredd4}.2f}")
    #När vi skrivit ut kvitto måste dessa nollställas eftersom det inte är säkert att nästa kund handlar exakt samma varor

#Huvudprogrammet i vilken alla av ovanstående funktioner utgör kassaapparaten
def kassa():
    objektslista = läs_från_fil("varudatabas.txt")
    lista_alla_koder = skapa_lista_alla_koder(objektslista)
    lista_skannade_koder = []
    print(f"\nBörja skanna genom att alltid ange varans kod fölt av mellsanslag och antalet du skannar följt av enter. Anger du inget antal är standard 1.\nVill du ta bort en vara matar du in varans kod följt av hur många du vill ta bort med ett minustecken framför.\nVill du ångra alla skannade artiklar anger du istället varans kod följt av enbart ett minustecken.\nFör kvittoutskrift, ange #.\nBörja här: ", end = "")
    inmatning = skanna_varor()
    while inmatning != "#":
        varukontroll = kontrollera_vara(inmatning,lista_alla_koder)
        if varukontroll == True:
            uppdateradlista = registrera_skannad_vara(inmatning, lista_alla_koder, lista_skannade_koder, objektslista)
            lista_skannade_koder = uppdateradlista
            inmatning = skanna_varor()
        else:
            inmatning = skanna_varor()
    skannade_varor = uppdatera_objektslista(objektslista,lista_skannade_koder,lista_alla_koder)
    längsta_strängar = bestäm_längsta_strängar(skannade_varor)
    print("")
    skriv_kvitto(skannade_varor,längsta_strängar)
    print("\nVälkommen åter!\n")
    skriv_till_fil(objektslista,"varudatabas.txt")

kassa()

