from array import array

class ArrayQ():
    def __init__(self):
        self.__newq = array('i')  
    def enqueue(self, x):  
        self.__newq.append(x)
    def dequeue(self):
        return self.__newq.pop(0)   
    def isEmpty(self): 
        if len(self.__newq) == 0:
            return True
        else:
            return False