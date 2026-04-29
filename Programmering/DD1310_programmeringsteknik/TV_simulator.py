from TV import TV #importerar TV klassen
#läser av filen 
def read_file(file_name):
    tvinfo = [] #Lista för att addera raderna från filen
    tvinfo2 = [] #lista för att lägga till TV-objekten
    file = open(file_name, "r")
    for line in file: #Gör så att tvinfo fylls på med informationen om tv-apparatrna från filen
        tvrad = []
        tvrad.append(line)
        tvrad = line.strip().split(",")
        tvinfo.append(tvrad)
    for i in range(len(tvinfo)): #Skapar lika många objekt som rader/längden av listan tvinfo
        name0 = tvinfo[i][0]
        name0 = TV(str(tvinfo[i][0]),int(tvinfo[i][1]),int(tvinfo[i][2]),int(tvinfo[i][3]),int(tvinfo[i][4])) #Skapar objekt med respektive namn
        tvinfo2.append(name0)
    
    file.close()
    return tvinfo2

#sparar informationen i textfilen
def write_file(list,file_name):
    file = open(file_name, "w")
    for tv in list:
        file.write(tv.str_for_file()+"\n") #Anropar str_for_file så att alla information läggs in i filen
    file.close()

#ändrar kanalen
def change_channel(tvobject):
    channel = input("\nAnge kanalnummer: ") #frågar vilken kanal man vill byta till
    while True:
        try:
            if tvobject.change_channel(int(channel)) == True: #kollar om det är en giltig kanal att byta till
                break
            else:
                channel = input(f"Kanal för den här TV:n ska vara mellan 1 till {tvobject.max_channel}, försök igen: ")
            #användning av try, except för felhantering
        except IndexError:
            channel = input(f"Kanal för den här TV:n ska vara mellan 1 till {tvobject.max_channel}, försök igen: ")
        except TypeError:
            channel = input(f"Kanal för den här TV:n ska vara mellan 1 till {tvobject.max_channel}, försök igen: ")
        except ValueError:
            channel = input(f"Kanal för den här TV:n ska vara mellan 1 till {tvobject.max_channel}, försök igen: ")

 #funktionern anropar metoden decrease_volume i TV klassen
def decrease_volume(tvobject):
    tvobject.decrease_volume()
    
 #funktionern anropar metoden increase_volume i TV klassen
def increase_volume(tvobject):
    tvobject.increase_volume()

def adjust_TV_menu(): #skriver ut möjliga alternativ för vad man vill göra (byta kanal, höj ljudnivå, sänk ljudnivå och återgå till huvudmeny)
    print("1. Byt kanal")
    print("2. Sänk ljudnivå")
    print("3. Höj ljudnivå")
    print("4. Återgå till huvudmenyn")
    choice = input("Välj: ") #tar en input som väljer vad som ska hända
    while True:
        try:
            if 0<int(choice)<=4: #felhantering
                return int(choice) #returnerar valet
            else:
                choice = input("Fel val, försök igen: ")
            #användning av try, except för felhantering
        except IndexError:
            choice = input("Fel val, försök igen: ")
        except TypeError:
            choice = input("Fel val, försök igen: ")
        except ValueError:
            choice = input("Fel val, försök igen: ")

def select_TV_menu(tvlista): #skriver ut tv objekten och avsluta som alternativ
    for i in range(len(tvlista)):
        print(f"{i+1}. {tvlista[i].name}")
    print(f"{len(tvlista)+1}. Avsluta")
    choice = input("Välj: ")
    while True:
        try:
            if int(choice)-1 == len(tvlista): #Personen i fråga har då valt Avsluta
                return None
              
            elif 0<=int(choice)-1<len(tvlista): #Personen har då valt något objekt                   
                return tvlista[(int(choice)-1)]

            else: 
                choice = input("Fel val, försök igen: ")
            #användning av try, except för felhantering
        except IndexError:
            choice = input("Fel val, försök igen: ")
        except TypeError:
            choice = input("Fel val, försök igen: ")
        except ValueError:
            choice = input("Fel val, försök igen: ")


     

#Huvudprogram:
def main():
    print("***Välkommen till TV-simulatorn****")
    tv_obj_list = read_file("resultat.txt")
    while True: #nästlad while loop så att man är fast i respektive meny tills man väljer att avbryta
        selected_tv = select_TV_menu(tv_obj_list) #anropar select tv menu och lagrar utdata i variabeln selected tv
        if selected_tv == None: #om man vill avsluta
            write_file(tv_obj_list, "resultat.txt") #sparar den ändrade infon i text filen
            break #avslutar hela programmet

        else:
            while True:
                print(selected_tv,"\n") #skriver ut infon för den tvapparat vi har valt
                tv_choice = adjust_TV_menu() #anropar adjust tv menu och lagrar utdata i tv choice
                if tv_choice == 1: #if sats som kollar val av adjust tv menu och anropar respektiva funktion 
                    change_channel(selected_tv) 
                    
                elif tv_choice == 2:
                    decrease_volume(selected_tv)
                    
                elif tv_choice == 3:
                    increase_volume(selected_tv)
                else:
                    print("")
                    break #går tillbaka till den yttre while loopen som är där man väljer tv apparat

main()