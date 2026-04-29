list1 = [["100","3"],["100","1"],["100","-2"]]
dellist = ["100","-2"]
string1 = "31"
string2 = "112"
string3 = f'{1111013.111222:.2f}'
string_list = [string1,string2,string3]

print(len(max(string_list, key=len)))

for a,b in list1:
    print(a) 
    print(b)