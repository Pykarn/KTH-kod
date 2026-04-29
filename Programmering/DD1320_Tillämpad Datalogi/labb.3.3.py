from bintreeFile import Bintree
def main():
    svenska = Bintree()
    with open("word3.txt", "r", encoding = "utf-8") as svenskfil:
        for rad in svenskfil:
            ordet = rad.strip()
            if ordet in svenska:
                pass
            else:
                svenska.put(ordet)   

    engelska = Bintree()
    with open("engelska.txt", "r", encoding="utf-8") as f:
        word_list = f.read().split()

    for word in word_list:
        word = word.strip(' !," ').lower()
        if word in engelska:
            pass
        else:
            engelska.put(word)
            if word in svenska:
                print(word, end = " ")

main()