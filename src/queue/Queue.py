# classe astratta
from abc import ABC, abstractmethod, abstractproperty
from queue import Queue
from Customer import Customer

class SuperMarketQueue(ABC):

    @abstractproperty
    def queue(self):
        return self._queue    

    @abstractmethod
    def enqueue(self, Customer c):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def first(self):
        pass
