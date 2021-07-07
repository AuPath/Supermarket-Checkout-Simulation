from enum import Enum

from mesa import Agent

from src.queue.SupermarketQueue import SupermarketQueue
from src.Customer import Customer
from abc import ABC, abstractmethod

PROCESSING_SPEED = 5


class CashDeskState(Enum):
    GET_NEW_CUSTOMER = 1
    PROCESSING_CUSTOMER = 2
    TRANSACTION_COMPLETED = 3


class CashDesk(ABC, Agent):

    @abstractmethod
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue, processing_speed=PROCESSING_SPEED):
        super().__init__(agent_id, model)

        self.__queue = supermarket_queue
        self.__customer: Customer = None
        self.__processing_speed = processing_speed
        self.__state = CashDeskState.GET_NEW_CUSTOMER

    @property
    def get_queue(self):
        return self.__queue

    def serve_new_customer(self):
        self.__customer = self.__queue.dequeue()

    def process_customer(self):
        self.get_customer().increase_processed_basket(self.__processing_speed)

    def complete_transaction(self):
        self.get_customer().complete_transaction()

    def get_customer(self):
        return self.__customer
