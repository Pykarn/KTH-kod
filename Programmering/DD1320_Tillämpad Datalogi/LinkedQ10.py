class Node:
    def __init__(self, data, next = None):
        self.data = data
        self.next = next


class LinkedQ:

    def __init__(self):
        self.__first = None
        self.__last = None

    def enqueue(self,data):
        newNode = Node(data)
        if self.__first == None: 
            self.__first = self.__last = newNode

        else: 
            self.__last.next = newNode
            self.__last = newNode
            
    def dequeue(self):
        first_data = self.__first.data
        self.__first = self.__first.next

        return first_data

    def isEmpty(self):
        if self.__first == None:
            return True
        else:
            return False
        
    def peek(self): #titta på första datan i kön
        if self.__first == None:
            return None
        return self.__first.data
    