import math
from abc import ABC, abstractmethod

from mesa import Agent

from src.Customer import Customer
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.State import State


class CashDesk(ABC, Agent):

    @abstractmethod
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue,
                 estimation_bias=False):
        super().__init__(agent_id, model)

        self.type = 2
        self.__queue = supermarket_queue
        self.__customer: Customer = None
        # Transaction time and break time parameters
        self.__processing_speed = 0
        self.a_transaction = 1
        self.b_transaction = 0
        self.a_break = 1
        self.b_break = 0
        self.estimation_bias = estimation_bias

    @property
    def queue(self):
        return self.__queue

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value: Customer):
        self.__customer = value

    @property
    def processing_speed(self):
        return self.__processing_speed

    @processing_speed.setter
    def processing_speed(self, value: int):
        self.__processing_speed = value

    @property
    def state(self):
        return self.__state

    def step(self):
        self.__state.action()

    def process_customer(self):
        c = self.customer

        self.processing_speed = self.service_time(c) / self.model.period_in_seconds

        if c.basket_size - self.__processing_speed <= 0:
            c.basket_size = 0
        else:
            c.basket_size -= self.__processing_speed

    def is_transaction_complete(self):
        return self.customer.basket_size == 0

    def state_change(self, new_state: State):
        self.__state = new_state

    def transaction_time(self, c: Customer):
        if c.basket_size == 0:
            return 0
        else:
            return math.exp(self.a_transaction * math.log(c.basket_size) + self.b_transaction)

    def estimate_transaction_time(self, c: Customer):
        if c.basket_size == 0:
            return 0
        else:
            return math.exp(self.a_transaction * math.log(c.estimate_basket_size()) + self.b_transaction)

    def break_time(self, c: Customer):
        if c.basket_size == 0:
            return 0
        else:
            return math.exp(self.a_break * math.log(c.basket_size) + self.b_break)

    def estimate_break_time(self, c: Customer):
        if c.basket_size == 0:
            return 0
        else:
            return math.exp(self.a_break * math.log(c.estimate_basket_size()) + self.b_break)

    def service_time(self, c: Customer):
        return self.estimate_transaction_time(c) + self.estimate_break_time(c)

    def service_time_total(self):
        total = 0
        for c in self.queue.content():
            total += self.service_time(c)

        if self.customer is not None:
            total += self.service_time(self.customer)

        return total

    def estimate_service_time_total(self):
        if self.estimation_bias:
            total = 0
            for c in self.queue.content():
                total += self.service_time(c)

            if self.customer is not None:
                total += self.service_time(self.customer)

            return total
        else:
            return self.service_time_total()

    def queue_size(self):
        if self.customer is not None:
            return self.queue.size() + 1
        else:
            return self.queue.size()

    def move_customer_beside_cashdesk(self):
        pass

    def advance(self, customer: Customer):
        pass

    def get_image(self):
        pass

    def total_items(self):
        if self.customer is not None:
            return self.queue.total_items() + self.customer.basket_size
        else:
            return self.queue.total_items()

    def estimate_total_items(self):
        if self.estimation_bias:
            if self.customer is not None:
                return self.queue.estimate_total_items() + self.customer.basket_size
            else:
                return self.queue.estimate_total_items()
        else:
            return self.total_items()

    def is_queue_full(self):
        return self.queue.size() >= self.model.max_customer_in_queue
