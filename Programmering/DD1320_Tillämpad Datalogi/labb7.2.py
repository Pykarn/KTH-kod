from hashtable import Hashtable

def main():
    hashtable = None
    
    while True:
        line = input()
        key, *value = line.split()
        if key == '#':
            print('#')
            break
        elif key == 'init' and len(value) > 0:
            size = int(value[0])
            hashtable = Hashtable(size)
            print('New size:', size)
        elif len(value) > 0:
            hashtable.store(key, value[0])
            print(key, '<-', value[0])
        else:
            try:
                value = hashtable.search(key)
                print(f'{key}: {value}')
            except KeyError:
                print('KeyError:', key)


if __name__ == "__main__":
    main()


"""
Varför hashning är snabb:
den beräknar direkt indexet i tabellen i stället för att jämföra många element

Hur krockar hanteras:
med linjär probning (går till nästa lediga plats)

Varför hashfunktionen fungerar bra:
sprider nycklar över hela tabellen (multiplikation med 32 och modulus)

Varför tabellen inte får vara full:
annars fastnar probningen i evig loop
"""