# trackid<SEP>låtid<SEP>artistnamn<SEP>låttitel
import timeit
from klassLåt import Låt

def read_file(filename, n=None):
    obj_lista = []
    with open(filename, "r", encoding="utf-8") as file:
        for i, rad in enumerate(file):
            if n is not None and i >= n:   # stoppa vid n rader
                break
            rad = rad.strip().split("<SEP>")
            låt = Låt(rad[0], rad[1], rad[2], rad[3])
            obj_lista.append(låt)
    return obj_lista


# trackid<SEP>låtid<SEP>artistnamn<SEP>låttitel

def binary_search(lst, key):
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == key:
            return lst[mid]   # skriv ut elementet
        elif lst[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return None                # om inte hittad


# def main():
#     #Läs in listan
#     indata = input().strip()
#     the_list = indata.split()
#     #Läs in nycklar att söka efter
#     key = input().strip()
#     while key != "#":
#         print(binary_search(the_list, key))
#         key = input().strip()
# main()

def linsok(lst, key):
    for song in lst:
        if song.låttitel == key:
            return song
    return None

def binsok(lst, key):
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid].låttitel == key:
            return lst[mid]   # skriv ut elementet
        elif lst[mid].låttitel < key:
            low = mid + 1
        else:
            high = mid - 1
    return None 

def build_dict(lst):
    
    return {song.låttitel: song for song in lst}

def hashsok(dic, key):
    
    return dic.get(key, None)


def linmain():

    filename = "unique_tracks.txt"

    lista = read_file(filename)
    n = len(lista)
    print("Antal element =", n)

    sista = lista[n-1]
    testartist = sista.låttitel

    linjtid = timeit.timeit(stmt = lambda: linsok(lista, testartist), number = 1000)
    print("Linjärsökningen tog", round(linjtid/1000, 10) , "sekunder")


linmain()

def binmain():

    filename = "unique_tracks.txt"

    lista = read_file(filename, 250000)

    lista.sort()

    n = len(lista)
    print("Antal element =", n)

    sista = lista[n-1]
    testartist = sista.låttitel

    bintid = timeit.timeit(stmt = lambda: binsok(lista, testartist), number = 1000)
    print("Binärsökningen tog", round(bintid/1000, 10) , "sekunder")

binmain()

def hashmain():
    filename = "unique_tracks.txt"
    lista = read_file(filename, 250000)
    n = len(lista)
    print("Antal element =", n)

    sista = lista[-1]
    testartist = sista.låttitel

    dic = build_dict(lista)

    hashtid = timeit.timeit(stmt=lambda: hashsok(dic, testartist), number=1000)
    print("Hashtabellssökningen tog", round(hashtid/1000, 10), "sekunder")

hashmain()


def bubble_sort(lst):
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j].låttitel > lst[j + 1].låttitel:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst



def heapify(lst, n, i):
    """ Hjälpfunktion för heapsort, bygger max-heap """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Jämför med vänster barn
    if left < n and lst[left].låttitel > lst[largest].låttitel:
        largest = left

    # Jämför med höger barn
    if right < n and lst[right].låttitel > lst[largest].låttitel:
        largest = right

    # Om största inte är roten → byt plats och heapify rekursivt
    if largest != i:
        lst[i], lst[largest] = lst[largest], lst[i]
        heapify(lst, n, largest)

def heapsort(lst):
    n = len(lst)

    # Bygg max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(lst, n, i)

    # Ta ut element från heap en och en
    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]  # byt
        heapify(lst, i, 0)

    return lst



def sortmain():
    filename = "unique_tracks.txt"
    
    lista = read_file(filename, n=1000)

    n = len(lista)
    print("Antal element =", n)

    # Kopiera listorna (så att de inte blir sorterade på förhand)
    lista1 = lista[:]
    lista2 = lista[:]

    # Bubble sort
    bubble_tid = timeit.timeit(stmt=lambda: bubble_sort(lista1), number=1)
    print("Bubble sort tog", round(bubble_tid, 4), "sekunder")

    # Heapsort
    heap_tid = timeit.timeit(stmt=lambda: heapsort(lista2), number=1)
    print("Heapsort tog", round(heap_tid, 4), "sekunder")



sortmain()