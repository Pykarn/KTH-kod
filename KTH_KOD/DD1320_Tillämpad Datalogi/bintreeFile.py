class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Bintree:
    def __init__(self):
        self.root = None
        
    def put(self,newvalue): # Sorterar in newvalue i trädet
        self.root = putta(self.root,newvalue)

    def __contains__(self,value): # True om value finns i trädet, False annars
        return finns(self.root,value)

    def write(self):
        # Skriver ut trädet i inorder
        skriv(self.root)
        print("\n")


#-------------- Hjälpfunktioner --------------

def putta(p, newvalue): # Funktion som gör själva jobbet att stoppa in en ny nod 
    if p == None:
        p = Node(newvalue)
        return p
    if newvalue < p.value:
        p.left =  putta(p.left,newvalue)
        return p
    if newvalue > p.value:
        p.right = putta(p.right,newvalue)
        return p

def finns(p,value): # Funktion som gör själva jobbet att söka efter ett värde
        if p == None: 
            return False
        if value == p.value: 
            return True
        if value < p.value:
            return finns(p.left,value)
        if value > p.value: 
            return finns(p.right,value)

def skriv(p): # Funktion som gör själva jobbet att skriva ut trädet
    if p != None:
        skriv(p.left)
        print(p.value)
        skriv(p.right)