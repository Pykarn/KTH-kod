class Node:
    def __init__(self, data, next = None):
        self.data = data
        self.next = next
        
class LinkedQ:
    def __init__(self):
        self.__first = None
        self.__last = None

    def enqueue(self, x):  
        ny = Node(x)
        if self.__first == None:
            self.__first = ny
            self.__last = ny
        else:
            self.__last.next = ny
            self.__last = ny


    def dequeue(self):
        data = self.__first.data
        self.__first = self.__first.next
        if self.__first == None:
            self.__last = None
        return data
        
    
    def isEmpty(self): 
        if self.__first == None:
            return True
        else:
            return False
