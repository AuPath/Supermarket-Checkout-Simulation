from Customer import Customer
from mesa import Model
from src.queue.SupermarketQueue import SupermarketQueue
from mesa.space import MultiGrid

ADJ_WINDOW_SIZE = 2


class Supermarket(Model):
    def __init__(self, customers: set[Customer], queues: list[SupermarketQueue], width, height, adj_window_size=ADJ_WINDOW_SIZE):
        self.__customers = customers
        self.__queues = queues
        self.grid = MultiGrid(width, height, True)

    def add_customer(self, customer: Customer):
        self.__customers.add(customer)

    def remove_customer(self, customer: Customer):
        self.__customers.remove(customer)

    def get_queues(self):
        return self.__queues

    def get_adj_queues(self, queue: SupermarketQueue, window_size: int):
        pass

    def get_valid_queues(self):
        pass
