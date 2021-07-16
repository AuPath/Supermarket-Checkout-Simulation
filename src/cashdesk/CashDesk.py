import logging
from abc import ABC, abstractmethod
from enum import Enum

from mesa import Agent

from src.Customer import Customer
from src.queue.SupermarketQueue import SupermarketQueue

PROCESSING_SPEED = 5


class CashDeskState(Enum):
    GET_NEW_CUSTOMER = 1
    PROCESSING_CUSTOMER = 2
    TRANSACTION_COMPLETED = 3


class CashDesk(ABC, Agent):

    @abstractmethod
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue, processing_speed=PROCESSING_SPEED):
        super().__init__(agent_id, model)

        self.type = 2
        self.__queue = supermarket_queue
        self.__customer: Customer = None
        self.__processing_speed = processing_speed
        self.__state = CashDeskState.GET_NEW_CUSTOMER

    @property
    def queue(self):
        return self.__queue

    def step(self):
        if self.__state == CashDeskState.GET_NEW_CUSTOMER:
            logging.info("Cash desk " + type(self).__name__ + " " + str(self.unique_id) + " searching for new customer")
            new_state = self.serve_new_customer()
            self.__state = new_state
        elif self.__state == CashDeskState.PROCESSING_CUSTOMER:
            logging.info("Cash desk " + type(self).__name__ + " " + str(self.unique_id) + " processing customer " + str(
                self.__customer.unique_id))
            if not self.__customer.transaction_is_completed():
                self.process_customer()
            else:
                logging.info(
                    "Cash desk " + type(self).__name__ + " " + str(self.unique_id) + " completing the transaction")
                self.__state = CashDeskState.TRANSACTION_COMPLETED
                self.complete_transaction()
                self.__state = CashDeskState.GET_NEW_CUSTOMER
        elif self.__state == CashDeskState.TRANSACTION_COMPLETED:
            self.complete_transaction()
            self.__state = CashDeskState.GET_NEW_CUSTOMER

    def serve_new_customer(self):
        if self.queue.size() > 0:
            self.__customer = self.__queue.dequeue()
            self.__customer.start_transaction()
            new_state = CashDeskState.PROCESSING_CUSTOMER

            # make every customer advance
            for customer in self.__queue.content():
                customer.advance()
        else:
            new_state = CashDeskState.GET_NEW_CUSTOMER
        return new_state

    def process_customer(self):
        self.get_customer().increase_processed_basket(self.__processing_speed)

    def complete_transaction(self):
        self.get_customer().complete_transaction()

    def get_customer(self):
        return self.__customer
