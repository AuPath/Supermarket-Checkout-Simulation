# classe astratta
from abc import ABC, abstractmethod, abstractproperty
from queue import Queue
from src.Customer import Customer

class SupermarketQueue(ABC):

    @abstractmethod
    @property
    def queue(self):
        return self.__queue    

    @abstractmethod
    def enqueue(self, c:Customer):
        pass

    @abstractmethod
    def dequeue(self):
        pass
    
