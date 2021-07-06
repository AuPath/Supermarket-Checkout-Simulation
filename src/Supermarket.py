import random

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from Customer import Customer
from OccupiedCell import OccupiedCell
from src.queue.SupermarketQueue import SupermarketQueue
from src.cashdesk.CashDesk import CashDesk

ADJ_WINDOW_SIZE = 2


class Supermarket(Model):

    def __init__(self, width, height, cash_desks: list[CashDesk], adj_window_size=ADJ_WINDOW_SIZE):
        self.__customers = set()
        self.__occupied_cells = set()
        self.__cash_desks = cash_desks
        self.grid = SingleGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.__adj_window_size = adj_window_size
        self.__counter = 0  # TODO: is needed to create agents, is there another way?
        self.running = True
        self.init_environment()

    def step(self):
        if self.__counter % 5 == 0:  # TODO: when do we have to create new agents? what is the maximum basket size?
            self.add_customer(
                Customer(len(self.__customers) + 1, self, random.randint(0, 50), bool(random.getrandbits(1))))
        self.schedule.step()
        self.__counter += 1

    def init_environment(self):
        # Entering zone
        x = self.grid.width - 3
        y = 0

        cell = self.add_occupied_cell(False)
        self.grid.place_agent(cell, (x, y))
        cell = self.add_occupied_cell(False)
        self.grid.place_agent(cell, (x, y + 1))

        # Cash desks
        x = 0
        for cash_desk in self.get_cash_desks():
            y = 1
            cell = self.add_occupied_cell(True)
            self.grid.place_agent(cell, (x, y))
            cell = self.add_occupied_cell(True)
            self.grid.place_agent(cell, (x, y + 1))

            x = x + 2

    def add_customer(self, customer: Customer):
        self.__customers.add(customer)
        self.schedule.add(customer)
        positioned = False

        while not positioned:
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if self.grid.is_cell_empty((x, y)):
                self.grid.place_agent(customer, (x, y))
                positioned = True

    def remove_customer(self, customer: Customer):
        self.__customers.remove(customer)

    def get_queues(self):
        return [cash_desk.get_queue() for cash_desk in self.__cash_desks]

    def get_unique_queues(self):
        return set(self.get_unique_queues())

    def get_adj_queues(self, queue: SupermarketQueue):
        pass

    def get_valid_queues(self):
        pass

    def get_occupied_cells(self):
        return self.__occupied_cells

    def add_occupied_cell(self, is_cash_desk):
        cell = OccupiedCell(len(self.get_occupied_cells()) + 1, self, is_cash_desk)
        self.__customers.add(cell)
        return cell

    def get_cash_desks(self):
        return self.__cash_desks