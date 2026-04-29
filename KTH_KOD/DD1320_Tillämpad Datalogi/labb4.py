from linkedQFile import LinkedQ
from bintreeFile import Bintree

# VERSION 1:
def makechildren1(startord):

    # --------INLÄSNING AV ORDLISTA--------
    svenska = Bintree()
    with open("word3.txt", "r", encoding = "utf-8") as svenskfil:
        for rad in svenskfil:
            ordet = rad.strip()
            if ordet not in svenska:
                svenska.put(ordet) 

    # --------Fråga efter slutord--------
    # slutord = input('Ange slutord: ')

    gamla = Bintree()
    alfabetet = 'abcdefghijklmnopqrstuvwxyzåäö'

    for i in range(len(startord)):
        for bokstav in alfabetet:
            if bokstav == startord[i]:
                continue  # hoppar bara över denna bokstav, fortsätter med nästa bokstav
            barn = startord[:i] + bokstav + startord[i+1:]

            if barn in svenska:
                if barn not in gamla:
                    gamla.put(barn)
                    print(barn,end = ' ')

#startord = input('Ange startord: ').strip().lower()
#makechildren1(startord)


# -------------------------------------------------------
# ANDRA VERSIONEN
def main():
    # --------INLÄSNING AV ORDLISTA--------
    svenska = Bintree()
    with open("word3.txt", "r", encoding = "utf-8") as svenskfil:
        for rad in svenskfil:
            ordet = rad.strip()
            if ordet not in svenska:
                svenska.put(ordet) 

    # --------Fråga efter startord och slutord--------
    startord = input('Ange startord: ').strip().lower()
    slutord = input('Ange slutord: ').strip().lower()

    gamla = Bintree()
    gamla.put(startord)
    q = LinkedQ()
    q.enqueue(startord) # Börjar med att köa stamfadern

    while not q.isEmpty():
        word = q.dequeue()

        q,found,gamla = makechildren(word, slutord, q, svenska, gamla)
        
        if found:
            return
        
    print("Det finns ingen väg till", slutord)


def makechildren(word, slutord, q, svenska, gamla):
    found = False
    alfabetet = 'abcdefghijklmnopqrstuvwxyzåäö'

    for i in range(len(word)):
        for bokstav in alfabetet:
            if bokstav == word[i]:
                continue  # hoppar bara över denna bokstav, fortsätter med nästa bokstav

            barn = word[:i] + bokstav + word[i+1:]

            if barn in svenska and barn not in gamla:
                if barn == slutord:
                    print("Det finns en väg till", slutord)
                    found = True
                    return None,found,None
                else:
                    gamla.put(barn)
                    q.enqueue(barn)

    return q,found,gamla

main()