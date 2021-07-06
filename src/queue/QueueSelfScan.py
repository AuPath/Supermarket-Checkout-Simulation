from src.SupermarketQueue import SupermarketQueue
from queue import Queue

class QueueSelfScan(SuperMarketQueue):

    def __init__(self):
        self.__queue = Queue()
        self.__partial_check_queue = Queue()

    def queue(self):
        super().queue()

    def enqueue(self, c:Customer):
        self.__queue.put(c)

    def dequeue(self):
        return self.__queue.get()

