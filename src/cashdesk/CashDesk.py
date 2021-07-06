from src.queue.SupermarketQueue import SupermarketQueue
from src.Customer import Customer
from abc import ABC, abstractmethod

PROCESSING_SPEED = 5


class CashDesk(ABC):

    @abstractmethod
    def __init__(self, supermarket_queue: SupermarketQueue, processing_speed=PROCESSING_SPEED):
        self.__queue = supermarket_queue
        self.__customer: Customer = None
        self.__processing_speed = processing_speed

    @property
    def get_queue(self):
        return self.__queue

    def serve_new_customer(self, customer: Customer):
        self.__customer = customer

    def process_customer(self):
        self.__customer.increase_processed_basket(self.__processing_speed)

    def complete_transaction(self):
        pass
