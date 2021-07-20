import math
from abc import ABC, abstractmethod

from mesa import Agent

from src.Customer import Customer
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.cashdeskstates.CashDeskStates import *
from src.states.State import State

PROCESSING_SPEED = 2


class CashDesk(ABC, Agent):

    @abstractmethod
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue, processing_speed=PROCESSING_SPEED):
        super().__init__(agent_id, model)

        self.type = 2
        self.__queue = supermarket_queue
        self.__customer: Customer = None
        self.__processing_speed = processing_speed
        self.__state = CashDeskNewCustomerState(self)
        # Transaction time and break time parameters
        self.a_transaction = 1
        self.b_transaction = 0
        self.a_break = 1
        self.b_break = 0

    @property
    def queue(self):
        return self.__queue

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value: Customer):
        self.__customer = value

    def step(self):
        self.__state.action()

    def process_customer(self):
        c = self.customer

        if c.basket_size - self.__processing_speed <= 0:
            c.basket_size = 0
        else:
            c.basket_size -= self.__processing_speed

    def is_transaction_complete(self):
        return self.customer.basket_size == 0

    def state_change(self, new_state: State):
        self.__state = new_state

    def transaction_time(self, c: Customer):
        return math.exp(self.a_transaction * math.log(c.basket_size) + self.b_transaction)

    def break_time(self, c: Customer):
        return math.exp(self.a_break * math.log(c.basket_size) + self.b_break)

    def service_time(self, c: Customer):
        return self.transaction_time(c) + self.break_time(c)

    def service_time_total(self):
        total = 0
        for c in self.queue.content():
            total += self.service_time(c)
        return total

    # todo rinomina in move_customer_besides_cashdesk, il customer come parametro non dovrebbe essere necessario in quanto lavora solo sul customer al cashdesk
    def move_beside(self):
        pass

    def advance(self, customer: Customer): # todo forse advance é un qualcosa di riservato per Mesa
        pass
