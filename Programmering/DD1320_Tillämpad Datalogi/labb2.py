from linkedQFile import LinkedQ
        
def main():
    q = LinkedQ()
    #[3,1,4,2,5]
    indata = input()
    numlist = indata.split()
    for i in numlist:
        q.enqueue(i)    
    list = []
    while q.isEmpty() == False:
        first1 = q.dequeue()
        q.enqueue(first1)
        first2 = q.dequeue()
        list.append(first2)  
    output = " ".join(list)
    return output

print(main())







