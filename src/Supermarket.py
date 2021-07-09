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
    """SuperMARCO model: description here"""

    def __init__(self, customers_metadata, cash_desks_metadata, entering_area_width, shopping_area_height,
                 adj_window_size=ADJ_WINDOW_SIZE):
        self.__customers = set()
        self.__occupied_cells = set()
        self.__cash_desks: list[CashDesk] = []
        self.grid = None
        self.customer_scheduler = RandomActivation(self)
        self.cash_desk_scheduler = RandomActivation(self)
        self.__adj_window_size = adj_window_size
        self.__num_agent = 0
        self.running = True
        self.queues = None
        self.entering_area_width = entering_area_width
        self.shopping_area_height = shopping_area_height
        # Create cash desks
        self.init_cash_desks(cash_desks_metadata)
        # Init grid
        self.init_environment()
        # Create customers
        self.init_customers(customers_metadata)

    def step(self):
        customer_to_remove = set()
        for customer in self.__customers:
            if customer.get_state() == CustomerState.SHOPPING:
                if not self.is_in_shopping_area(customer):
                    position = self.get_shopping_area_position()
                    if self.grid.is_cell_empty(position):
                        self.grid.move_agent(customer, position)
                        return

            if customer.get_state == CustomerState.EXITING:
                customer_to_remove.add(customer)
        for to_remove in customer_to_remove:
            self.remove_customer(to_remove)

        self.customer_scheduler.step()
        self.cash_desk_scheduler.step()

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
        x = self.grid.width - self.entering_area_width
        for y in range(0, self.grid.height - self.shopping_area_height):
            cell = self.add_occupied_cell(False, "v")
            self.grid.place_agent(cell, (x, y))

        # Shopping zone
        y = self.grid.height - self.shopping_area_height
        for x in range(0, self.grid.width - self.entering_area_width):
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
        self.cash_desk_scheduler.add(cash_desks)

    def add_customer(self, customer: Customer):
        self.__customers.add(customer)
        self.customer_scheduler.add(customer)
        positions = [(self.grid.width - 2, 0), (self.grid.width - 1, 0), (self.grid.width - 2, 1),
                     (self.grid.width - 1, 1)]

        for position in positions:
            # Add the agent to the entering zone of the market
            if self.grid.is_cell_empty(position):
                self.grid.place_agent(customer, position)
                return

    def remove_customer(self, customer: Customer):
        self.__customers.remove(customer)
        self.customer_scheduler.remove(customer)
        self.grid.remove_agent(customer)

    @property
    def queues(self):
        return [cash_desk.queue for cash_desk in self.__cash_desks]

    @queues.setter
    def queues(self, value):
        self._queues = value

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

    def is_in_shopping_area(self, customer: Customer):
        (x, y) = customer.pos
        if self.grid.height - self.shopping_area_height < y <= self.grid.height:
            return True
        return False

    def get_shopping_area_position(self):
        return self.random.randrange(self.grid.width), self.random.randrange(
            self.grid.height - self.shopping_area_height + 1, self.grid.height)
