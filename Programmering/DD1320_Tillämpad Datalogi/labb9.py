#Labb 9
from LinkedQ9 import LinkedQ
import unittest

ptable = "H  He  Li  Be  B   C   N   O   F   Ne  Na  Mg  Al  Si  P   S   Cl  Ar  K   Ca  Sc  Ti  V   Cr Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr  Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd In  Sn  Sb  Te  I   Xe  Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn  Fr  Ra  Ac  Th  Pa  U   Np  Pu  Am  Cm Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Fl  Lv"
atomlista = ptable.split()

#läsformel() --> läsmol() --> läsgrupp() och sedan eventuellt sej själv 
#(men inte om inmatningen är slut eller om den just kommit tillbaka från ett parentesuttryck).

#läsgrupp() --> läsatom() eller läsgrupp() --> läsmol()

class Syntaxfel(Exception):
    pass


def läsFormel(kö):
    if kö.isEmpty():
        raise Syntaxfel("Felaktig gruppstart vid radslutet")
    läsMol(kö)
    if not kö.isEmpty():
        tecken = ""
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("Felaktig gruppstart vid radslutet " + tecken)

def läsMol(kö):
    läsGrupp(kö)
    if not kö.isEmpty() and kö.peek() != ")":
        läsMol(kö)

def läsGrupp(kö):
    if kö.peek() == "(":
        kö.dequeue()
        läsMol(kö)
        if kö.isEmpty():
            raise Syntaxfel("Saknad högerparentes vid radslutet")
        if kö.peek() == ")":
            kö.dequeue()
            läsNummer(kö)
            return

    if not kö.isEmpty() and not kö.peek().isalpha():
        tecken = ""
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("Felaktig gruppstart vid radslutet" + " " + tecken)

    if not kö.isEmpty():
        atom = läsAtom(kö)
        if atom not in atomlista:
            tecken = ""
            while not kö.isEmpty():
                tecken += kö.dequeue()
            raise Syntaxfel("Okänd atom vid radslutet" + " " + tecken)
        if not kö.isEmpty() and kö.peek().isdigit():
            läsNummer(kö)

def läsAtom(kö):
    tecken1 = läsLETTER(kö) 
    if kö.isEmpty():
        return tecken1

    if kö.peek().islower() and kö.peek().isalpha():
        tecken2 = läsLetter(kö)
        return tecken1+tecken2
    return tecken1

def läsLETTER(kö): #Stor bokstav
    tecken = kö.dequeue()

    if tecken.isupper() and tecken.isalpha():
        return tecken #Godkänt
    while not kö.isEmpty():
        tecken += kö.dequeue()
    raise Syntaxfel("Saknad stor bokstav vid radslutet" + " " + tecken)

def läsLetter(kö): #Liten bokstav
    tecken = kö.dequeue()
    if tecken.islower():
        return tecken
    raise Syntaxfel("Mer än en stor bokstav")

def läsNummer(kö):
    if kö.isEmpty():
        raise Syntaxfel("Saknad siffra vid radslutet")
    
    siffra = kö.dequeue()
    tecken = ""

    if not siffra.isdigit():
        tecken = siffra
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("Saknad siffra vid radslutet" + " " + tecken)

    if siffra == "0":
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("För litet tal vid radslutet" + " " + tecken)

    while not kö.isEmpty() and kö.peek().isdigit():
        siffra += kö.dequeue()
    if int(siffra) >= 2:
        return
    while not kö.isEmpty():
        tecken += kö.dequeue()
    raise Syntaxfel("För litet tal vid radslutet" + " " + tecken)

def kontrolleraFormel(kö):
    try:
        läsFormel(kö)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as fel:
        return str(fel).strip()

def lagraFormel(molekyl):
    kö = LinkedQ()
    for i in range(len(molekyl)): #Köar varje tecken
        kö.enqueue(molekyl[i]) 
    return kö

def main():
    molekyl = input("Ange molekyl: ")
    while molekyl != "#":
        kö = lagraFormel(molekyl)
        resultat = kontrolleraFormel(kö)
        print(resultat)
        molekyl = input("Ange molekyl: ")

main()

class Test1(unittest.TestCase):

    def test_1(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("Na")), "Formeln är syntaktiskt korrekt")
    def test_2(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("H2O")), "Formeln är syntaktiskt korrekt")
    def test_3(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("Si(C3(COOH)2)4(H2O)7")), "Formeln är syntaktiskt korrekt")
    def test_4(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("Na332")), "Formeln är syntaktiskt korrekt")


class Test2(unittest.TestCase):
    def test_5(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("C(Xx4)5")), "Okänd atom vid radslutet 4)5")
    def test_6(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("C(OH4)C")), "Saknad siffra vid radslutet C")
    def test_7(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("C(OH4C")), "Saknad högerparentes vid radslutet")
    def test_8(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("H2O)Fe")), "Felaktig gruppstart vid radslutet )Fe")
    def test_9(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("H0")), "För litet tal vid radslutet")
    def test_10(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("H1C")), "För litet tal vid radslutet C")
    def test_11(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("H02C")), "För litet tal vid radslutet 2C")
    def test_12(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("Nacl")), "Saknad stor bokstav vid radslutet cl")
    def test_13(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("a")), "Saknad stor bokstav vid radslutet a")
    def test_14(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("(Cl)2)3")), "Felaktig gruppstart vid radslutet )3")
    def test_15(self):
        self.assertEqual(kontrolleraFormel(lagraFormel(")")), "Felaktig gruppstart vid radslutet )")
    def test_16(self):
        self.assertEqual(kontrolleraFormel(lagraFormel("2")), "Felaktig gruppstart vid radslutet 2")

if __name__ == "__main__":
    unittest.main()
