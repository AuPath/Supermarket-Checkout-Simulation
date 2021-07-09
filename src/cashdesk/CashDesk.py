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
    def queue(self):
        return self.__queue

    def step(self):
        if self.__state == CashDeskState.GET_NEW_CUSTOMER:
            new_state = self.serve_new_customer()
            self.__state = new_state
        elif self.__state == CashDeskState.PROCESSING_CUSTOMER:
            if not self.__customer.transaction_is_completed():
                self.process_customer()
            else:
                self.__state = CashDeskState.TRANSACTION_COMPLETED
        elif self.__state == CashDeskState.TRANSACTION_COMPLETED:
            self.complete_transaction()
            self.__state = CashDeskState.GET_NEW_CUSTOMER

    def serve_new_customer(self):
        if self.queue.size() > 0:
            self.__customer = self.__queue.dequeue()
            self.__customer.start_transaction()
            new_state = CashDeskState.PROCESSING_CUSTOMER
        else:
            new_state = CashDeskState.GET_NEW_CUSTOMER
        return new_state

    def process_customer(self):
        self.get_customer().increase_processed_basket(self.__processing_speed)

    def complete_transaction(self):
        self.get_customer().complete_transaction()

    def get_customer(self):
        return self.__customer
