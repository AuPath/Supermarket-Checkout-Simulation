from abc import ABC, abstractmethod
from queue import Queue

from mesa import Agent

from src.Customer import Customer


class SupermarketQueue(ABC, Agent):

    @abstractmethod
    def __init__(self):
        self.__queue = Queue()

    def enqueue(self, c: Customer):
        self.__queue.put(c)

    def dequeue(self):
        return self.__queue.get()

    def size(self):
        return self.__queue.qsize()

    def contains(self, c: Customer):

        for x in self.content():
            if x == c:
                return True
        return False

    def content(self):
        new_queue = Queue()

        l = []
        while self.__queue.qsize() > 0:
            element = self.__queue.get()
            new_queue.put(element)
            l.append(element)

        self.__queue = new_queue
        return l

    def total_items(self):
        return sum([1 for _ in self.content()])
