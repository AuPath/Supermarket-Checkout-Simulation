from src.SupermarketQueue import SupermarketQueue
from queue import Queue

class QueueSelfScan(SuperMarketQueue):

    def __init__(self):
        super().__init__(self)
        self.__partial_check_queue = Queue()

    def queue(self):
        super().queue()

    def enqueue(self, c:Customer):
        super().enqueue(c)

    def dequeue(self):
        return super().dequeue()

