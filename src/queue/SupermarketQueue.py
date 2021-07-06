# classe astratta
from abc import ABC, abstractmethod, abstractproperty
from queue import Queue
from src.Customer import Customer


class SupermarketQueue(ABC):

    @abstractmethod
    def __init__(self):
        self.__queue = Queue()

    @abstractmethod
    def enqueue(self, c:Customer):
        self.__queue.put(c)

    @abstractmethod
    def dequeue(self):
        return self.__queue.get()

    @abstractmethod
    def size(self):
        return self.__queue.qsize()
