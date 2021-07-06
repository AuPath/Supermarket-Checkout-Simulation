from src.queue.SupermarketQueue import SupermarketQueue
from src.Customer import Customer
from abc import ABC, abstractmethod, abstractproperty


class CashDesk(ABC):

    @abstractmethod
    def __init__(self, supermarket_queue: SupermarketQueue):
        self.__queue = supermarket_queue
        self.__customer = None


    def serve_new_customer(self, customer: Customer):
        self.__customer = customer

