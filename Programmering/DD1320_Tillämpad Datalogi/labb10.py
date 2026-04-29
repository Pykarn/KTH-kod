from LinkedQ9 import LinkedQ
from molgrafik import *

# class Ruta:
#     def __init__(self, atom="()", num=1):
#         self.atom = atom
#         self.num = num
#         self.next = None
#         self.down = None

ptable = "H  He  Li  Be  B   C   N   O   F   Ne  Na  Mg  Al  Si  P   S   Cl  Ar  K   Ca  Sc  Ti  V   Cr Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr  Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd In  Sn  Sb  Te  I   Xe  Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn  Fr  Ra  Ac  Th  Pa  U   Np  Pu  Am  Cm Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Fl  Lv"
atomlista = ptable.split()

class Syntaxfel(Exception):
    pass

def läsFormel(kö):
    if kö.isEmpty(): # Om indatan är tom
        raise Syntaxfel("Felaktig gruppstart vid radslutet")
    mol = läsMol(kö)
    if not kö.isEmpty():
        tecken = ""
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("Felaktig gruppstart vid radslutet " + tecken)
    return mol

def läsMol(kö):
    mol = läsGrupp(kö)
    if not kö.isEmpty() and kö.peek() != ")":
        mol.next = läsMol(kö)
    return mol
    
def läsGrupp(kö):
    rutan = Ruta()
    if kö.peek() == "(":
        kö.dequeue()
        delmolekyl = läsMol(kö)
        rutan.down = delmolekyl
        if kö.isEmpty(): # Ifall kön är tom och ingen högerparentes angivits
            raise Syntaxfel("Saknad högerparentes vid radslutet")
        if kö.peek() == ")":
            kö.dequeue()
            rutan.num = läsNummer(kö)
            return rutan

    if not kö.isEmpty() and not kö.peek().isalpha(): # Om vi startar med en siffra eller "("
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
        rutan.atom = atom
        if not kö.isEmpty() and kö.peek().isdigit():
            num = läsNummer(kö)
            rutan.num = num
        return rutan
            
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
    
    num = kö.dequeue()
    tecken = ""

    if not num.isdigit():
        tecken = num
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("Saknad siffra vid radslutet" + " " + tecken)

    if num == "0":
        while not kö.isEmpty():
            tecken += kö.dequeue()
        raise Syntaxfel("För litet tal vid radslutet" + " " + tecken)

    while not kö.isEmpty() and kö.peek().isdigit():
        num += kö.dequeue()
    if int(num) >= 2:
        return int(num) # Godkänt nummer
    while not kö.isEmpty(): # För litet tal men inte noll i början
        tecken += kö.dequeue()
    raise Syntaxfel("För litet tal vid radslutet" + " " + tecken)

def kontrolleraFormel(kö):
    try:
        mol = läsFormel(kö)
        print("Formeln är syntaktiskt korrekt")
        return mol
    except Syntaxfel as fel:
        print(str(fel).strip())

def lagraFormel(molekyl):
    kö = LinkedQ()
    for i in range(len(molekyl)): #Köar varje tecken
        kö.enqueue(molekyl[i]) 
    return kö

def main():
    molekyl = input("Ange molekyl: ")
    while molekyl != "#":
        kö = lagraFormel(molekyl)
        mol = kontrolleraFormel(kö)
        mg = Molgrafik()
        mg.show(mol)
        molekyl = input("Ange molekyl: ")

main()

def skapaAtomdictionary():
    """Skapar och returnerar en lista med Atom-objekt"""
    atomdata = "H  1.00794;\
    He 4.002602;\
    Li 6.941;\
    Be 9.012182;\
    B  10.811;\
    C  12.0107;\
    N  14.0067;\
    O  15.9994;\
    F  18.9984032;\
    Ne 20.1797;\
    Na 22.98976928;\
    Mg 24.3050;\
    Al 26.9815386;\
    Si 28.0855;\
    P  30.973762;\
    S  32.065;\
    Cl 35.453;\
    K  39.0983;\
    Ar 39.948;\
    Ca 40.078;\
    Sc 44.955912;\
    Ti 47.867;\
    V  50.9415;\
    Cr 51.9961;\
    Mn 54.938045;\
    Fe 55.845;\
    Ni 58.6934;\
    Co 58.933195;\
    Cu 63.546;\
    Zn 65.38;\
    Ga 69.723;\
    Ge 72.64;\
    As 74.92160;\
    Se 78.96;\
    Br 79.904;\
    Kr 83.798;\
    Rb 85.4678;\
    Sr 87.62;\
    Y  88.90585;\
    Zr 91.224;\
    Nb 92.90638;\
    Mo 95.96;\
    Tc 98;\
    Ru 101.07;\
    Rh 102.90550;\
    Pd 106.42;\
    Ag 107.8682;\
    Cd 112.411;\
    In 114.818;\
    Sn 118.710;\
    Sb 121.760;\
    I  126.90447;\
    Te 127.60;\
    Xe 131.293;\
    Cs 132.9054519;\
    Ba 137.327;\
    La 138.90547;\
    Ce 140.116;\
    Pr 140.90765;\
    Nd 144.242;\
    Pm 145;\
    Sm 150.36;\
    Eu 151.964;\
    Gd 157.25;\
    Tb 158.92535;\
    Dy 162.500;\
    Ho 164.93032;\
    Er 167.259;\
    Tm 168.93421;\
    Yb 173.054;\
    Lu 174.9668;\
    Hf 178.49;\
    Ta 180.94788;\
    W  183.84;\
    Re 186.207;\
    Os 190.23;\
    Ir 192.217;\
    Pt 195.084;\
    Au 196.966569;\
    Hg 200.59;\
    Tl 204.3833;\
    Pb 207.2;\
    Bi 208.98040;\
    Po 209;\
    At 210;\
    Rn 222;\
    Fr 223;\
    Ra 226;\
    Ac 227;\
    Pa 231.03588;\
    Th 232.03806;\
    Np 237;\
    U  238.02891;\
    Am 243;\
    Pu 244;\
    Cm 247;\
    Bk 247;\
    Cf 251;\
    Es 252;\
    Fm 257;\
    Md 258;\
    No 259;\
    Lr 262;\
    Rf 265;\
    Db 268;\
    Hs 270;\
    Sg 271;\
    Bh 272;\
    Mt 276;\
    Rg 280;\
    Ds 281;\
    Cn 285"

    lista = atomdata.split(";")
    atomdict = dict()
    for data in lista:
        namn_vikt = data.split()
        namn = namn_vikt[0]
        vikt = float(namn_vikt[1])
        atomdict[namn] = vikt

    return atomdict



atomdict = skapaAtomdictionary()
def vikt(mol):
    if mol is None:
        return 0
    #om det är en atom
    molekylvikt = 0
    if mol.atom != "()":  #dvs inte en parentesnod
        molekylvikt += atomdict[mol.atom] * mol.num
    #om det finns något "under" (inom parentes)
    if mol.down:
        molekylvikt += mol.num * vikt(mol.down)
    #om det finns något "efter" (på samma nivå)
    molekylvikt += vikt(mol.next)
    return molekylvikt

def beräknaVikt():
    molekyl = input("Ange molekyl: ")
    kö = lagraFormel(molekyl)
    mol = läsFormel(kö)
    print(vikt(mol))


beräknaVikt()