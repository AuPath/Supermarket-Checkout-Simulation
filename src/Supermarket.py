import random

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from Customer import Customer, CustomerState
from OccupiedCell import OccupiedCell
from src.cashdesk.CashDesk import CashDesk
from src.cashdesk.CashDeskStandard import CashDeskStandard
from src.queue.SupermarketQueue import SupermarketQueue

ADJ_WINDOW_SIZE = 2

GRID_HEIGHT = 10


class Supermarket(Model):
    """Supermarket model: description here"""
    def __init__(self, customers_metadata, cash_desks_metadata, adj_window_size=ADJ_WINDOW_SIZE):
        self.__customers = set()
        self.__occupied_cells = set()
        self.__cash_desks : list[CashDesk] = []
        self.grid = None
        self.__schedule = RandomActivation(self)
        self.__adj_window_size = adj_window_size
        self.__num_agent = 0
        self.running = True
        # Create cash desks
        self.init_cash_desks(cash_desks_metadata)
        # Init grid
        self.init_environment()
        # Create customers
        self.init_customers(customers_metadata)

    def step(self):
        for customer in self.__customers:
            if customer.get_state() == CustomerState.EXITING:
                self.remove_customer(customer)

        self.__schedule.step()

    def init_customers(self, customers_metadata):
        for basket_size, self_scan, queue_choice_strategy in customers_metadata:
            customer = Customer(self.__num_agent, self, basket_size, self_scan, queue_choice_strategy)
            self.__num_agent += 1
            self.add_customer(customer)

    def init_cash_desks(self, cash_desks_metadata):
        for idx, queue in enumerate(cash_desks_metadata):
            # TODO: Generalize CashDesk type
            cash_desk = CashDeskStandard(idx, self, queue)
            self.add_cash_desk(cash_desk)

    def init_environment(self):
        # Build grid
        self.init_grid()
        # Fill grid
        self.fill_grid()

    def init_grid(self):
        width = len(self.__cash_desks) * 2 + 3
        height = GRID_HEIGHT
        self.grid = SingleGrid(width, height, False)

    def fill_grid(self):
        # Entering zone
        x = self.grid.width - 3
        for y in range(0, self.grid.height - 3):
            cell = self.add_occupied_cell(False, "v")
            self.grid.place_agent(cell, (x, y))

        # Shopping zone
        y = self.grid.height - 3
        for x in range(0, self.grid.width - 3):
            cell = self.add_occupied_cell(False, "h")
            self.grid.place_agent(cell, (x, y))

        # Cash desks
        x = 0
        for cash_desk in self.get_cash_desks():
            y = 1
            cell = self.add_occupied_cell(True)
            self.grid.place_agent(cell, (x, y))
            cell = self.add_occupied_cell(True)
            self.grid.place_agent(cell, (x, y + 1))

            x = x + 2

    def add_cash_desk(self, cash_desks):
        self.__cash_desks.append(cash_desks)

    def add_customer(self, customer: Customer):
        self.__customers.add(customer)
        self.__schedule.add(customer)
        positions = [(self.grid.width - 2, 0), (self.grid.width - 1, 0), (self.grid.width - 2, 1),
                     (self.grid.width - 1, 1)]

        for position in positions:
            # Add the agent to the entering zone of the market
            if self.grid.is_cell_empty(position):
                self.grid.place_agent(customer, position)
                return

    def remove_customer(self, customer: Customer):
        self.__customers.remove(customer)
        self.__schedule.remove(customer)
        self.grid.remove_agent(customer)

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

    def add_occupied_cell(self, is_cash_desk, direction=""):
        cell = OccupiedCell(len(self.get_occupied_cells()) + 1, self, is_cash_desk, direction)
        self.__occupied_cells.add(cell)
        return cell

    def get_cash_desks(self):
        return self.__cash_desks
