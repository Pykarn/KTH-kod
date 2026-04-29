from linkedQFile import LinkedQ
from bintreeFile import Bintree

class ParentNode: 
    def __init__(self, word, parent = None):
        self.word = word
        self.parent = parent
        

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
    stamfar = ParentNode(startord)
    q.enqueue(stamfar) # Börjar med att köa stamfadern

    while not q.isEmpty():
        word = q.dequeue()

        q,found,gamla = makechildren(word, slutord, q, svenska, gamla)
        
        if found:

            return
        
    print("Det finns ingen väg till", slutord)



def makechildren(word, slutord, q, svenska, gamla):
    found = False
    alfabetet = 'abcdefghijklmnopqrstuvwxyzåäö'

    parent = word.word

    for i in range(len(parent)):
        for bokstav in alfabetet:
            if bokstav == parent[i]:
                continue  # hoppar bara över denna bokstav, fortsätter med nästa bokstav

            barn = parent[:i] + bokstav + parent[i+1:]
            newnode = ParentNode(barn,word)

            if barn in svenska and barn not in gamla:
                if barn == slutord:                   
                    writechain(newnode)
                    found = True
                    return None,found,None
                else:
                    gamla.put(barn)
                    q.enqueue(newnode)

    return q,found,gamla

def writechain(slutord):

    if slutord.parent != None:
        writechain(slutord.parent)
        print(slutord.word)
    else:
        print(slutord.word)


main()