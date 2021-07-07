# classe astratta
from abc import ABC, abstractmethod, abstractproperty
from queue import Queue
from mesa import Agent
from src.Customer import Customer

class SupermarketQueue(ABC, Agent):

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

    # True if c is in the queue, False otherwise
    @abstractmethod
    def contains(self, c:Customer):

        for x in self.content(self):
            if x == c:
                return True
        return False    

    # Returns an ordered list of the Customers in the queue
    @abstractmethod
    def content(self):
        l = []

        while self.__queue.qsize() > 0:
            l.append(self.__queue.get())

        return l

    @abstractmethod
    def total_items(self):
        bskt_size = 0
        for c in self.content():
            bskt_size += c.basket_size

        return bskt_size
