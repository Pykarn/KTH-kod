#Labb 8
from LinkedQlab8 import LinkedQ
import unittest

class Syntaxfel(Exception):
    pass

def läsMolekyl(kö):
    läsAtom(kö) # Läs in atom
    if kö.peek() == None:
        return 
    strTal = ""
    while not kö.isEmpty():
        strTal += kö.dequeue()
    läsNummer(strTal)

def läsAtom(kö):
    läsLETTER(kö) #Läs in stor bokstav
    if kö.peek() == None: #då är vi klara
        return
    if kö.peek().isalpha(): #en till bokstav
        läsLetter(kö)

def läsLETTER(kö): # Stor bokstav
    tecken = kö.dequeue()
    if tecken.isupper() and tecken.isalpha():
        return # Godkänt
    while not kö.isEmpty():
        tecken += kö.dequeue()
    raise Syntaxfel("Saknad stor bokstav vid radslutet" + " " + tecken)
    
def läsLetter(kö): # Liten bokstav
    tecken = kö.dequeue()
    if tecken.islower():
        return
    raise Syntaxfel("Mer än en stor bokstav")

def läsNummer(strTal):
    if strTal[0] == "0":
        raise Syntaxfel("För litet tal vid radslutet" + " " + strTal[1:])
    if int(strTal) >= 2:
        return
    raise Syntaxfel("För litet tal vid radslutet" + " " + strTal[1:])
    
def kontrolleraMolekyl(kö):
    try:
        läsMolekyl(kö)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        return str(fel).strip()
    
def lagraMolekyl(molekyl):
    kö = LinkedQ()
    for i in range(len(molekyl)): # Köar varje tecken
        kö.enqueue(molekyl[i]) 
    return kö

def test(molekyl):
    kö = lagraMolekyl(molekyl)
    resultat = kontrolleraMolekyl(kö)
    return resultat

def main(molekyl=None):
    molekyl = input(" - Ange molekyl: ")
    while molekyl != "#":
        kö = lagraMolekyl(molekyl)
        resultat = kontrolleraMolekyl(kö)
        print(resultat)
        molekyl = input(" - Ange molekyl: ")

#main()


class SyntaxTest(unittest.TestCase):

    def testkorrekt(self):
        self.assertEqual(test("C4"), "Formeln är syntaktiskt korrekt")
    
    def testLETTER(self):
        self.assertEqual(test("2"), "Saknad stor bokstav vid radslutet 2")

    def testLetter(self):
        self.assertEqual(test("CC"), "Mer än en stor bokstav")
    
    def testNummer1(self):
        self.assertEqual(test("Cr02"), "För litet tal vid radslutet 2")
    
    def testNummer2(self):
        self.assertEqual(test("Cr1"), "För litet tal vid radslutet")




    


if __name__ == '__main__':
    unittest.main()