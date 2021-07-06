from src.Customer import Customer
from src.queue.SupermarketQueue import SupermarketQueue
from queue import Queue


class NormalQueue(SupermarketQueue):

    def __init__(self):
        self.__queue = Queue()

    def enqueue(self, c: Customer):
        super.enqueue()

    def dequeue(self):
        return super.dequeue()

    def size(self):
        return super.size()
