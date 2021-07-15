import math

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from src.Customer import Customer, CustomerState
from src.OccupiedCell import OccupiedCell, CashDeskType
from src.cashdesk.CashDesk import CashDesk
from src.cashdesk.CashDeskReserved import CashDeskReserved
from src.cashdesk.CashDeskSelfScan import CashDeskSelfScan
from src.cashdesk.CashDeskSelfService import CashDeskSelfService
from src.cashdesk.CashDeskStandard import CashDeskStandard
from src.queue.NormalQueue import NormalQueue
from src.queue.SupermarketQueue import SupermarketQueue
from src.zones.dinamic.CashDeskReservedZone import CashDeskReservedZone
from src.zones.dinamic.CashDeskSelfScanZone import CashDeskSelfScanZone
from src.zones.dinamic.CashDeskSelfServiceZone import CashDeskSelfServiceZone
from src.zones.dinamic.CashDeskStandardZone import CashDeskStandardZone
from src.zones.stationary.EnteringZone import EnteringZone
from src.zones.stationary.ShoppingZone import ShoppingZone

ADJ_WINDOW_SIZE = 2

GRID_HEIGHT = 20


class Supermarket(Model):
    """SuperMARCO model: description here"""

    def __init__(self, customers_metadata, zones_metadata, adj_window_size=ADJ_WINDOW_SIZE):
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
        self.zones_metadata = zones_metadata
        # Create zones
        self.entering_zone = None
        self.shopping_zone = None
        self.cash_desk_standard_zone = None
        self.cash_desk_self_service_zone = None
        self.cash_desk_self_scan_zone = None
        self.cash_desk_reserved_zone = None
        self.init_zones()
        # Create cash desks
        self.init_cash_desks()
        # Init grid
        self.init_environment()
        # Create customers
        self.init_customers(customers_metadata)

    def step(self):
        self.customer_scheduler.step()
        self.cash_desk_scheduler.step()

    def init_customers(self, customers_metadata):
        for basket_size, self_scan, queue_choice_strategy in customers_metadata:
            customer = Customer(self.__num_agent, self, basket_size, self_scan, queue_choice_strategy)
            self.__num_agent += 1
            self.add_customer(customer)

    def init_zones(self):
        for zone_type, dimension in self.zones_metadata:
            if zone_type == 'ENTERING':
                self.entering_zone = EnteringZone(self, dimension)
            elif zone_type == 'SHOPPING':
                self.shopping_zone = ShoppingZone(self, dimension)
            elif zone_type == 'CASH_DESK_STANDARD':
                self.cash_desk_standard_zone = CashDeskStandardZone(self, dimension)
            elif zone_type == 'CASH_DESK_SELF_SERVICE':
                self.cash_desk_self_service_zone = CashDeskSelfServiceZone(self, dimension)
            elif zone_type == 'CASH_DESK_SELF_SCAN':
                self.cash_desk_self_scan_zone = CashDeskSelfScanZone(self, dimension)
            elif zone_type == 'CASH_DESK_RESERVED':
                self.cash_desk_reserved_zone = CashDeskReservedZone(self, dimension)
            else:
                pass

    def init_cash_desks(self):
        idx = 1
        for zone_type, dimension in self.zones_metadata:
            if zone_type == 'CASH_DESK_STANDARD':
                for i in range(dimension):
                    cash_desk = CashDeskStandard(idx, self, NormalQueue())
                    self.cash_desk_standard_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
            elif zone_type == 'CASH_DESK_SELF_SERVICE':
                for i in range(dimension):
                    cash_desk = CashDeskSelfService(idx, self, NormalQueue())
                    self.cash_desk_self_service_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
            elif zone_type == 'CASH_DESK_SELF_SCAN':
                for i in range(dimension):
                    cash_desk = CashDeskSelfScan(idx, self, NormalQueue())
                    self.cash_desk_self_scan_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
            elif zone_type == 'CASH_DESK_RESERVED':
                for i in range(dimension):
                    cash_desk = CashDeskReserved(idx, self, NormalQueue())
                    self.cash_desk_reserved_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
            else:
                pass

    def init_environment(self):
        # Build grid
        self.init_grid()
        # Fill grid
        self.fill_grid()

    def init_grid(self):
        height = GRID_HEIGHT
        number_self_scan_left = max(0, self.cash_desk_self_scan_zone.cash_desks_number - math.ceil((height - self.shopping_zone.dimension - 1) / 2)) if self.cash_desk_self_scan_zone is not None else 0
        width = 2 + 1 + number_self_scan_left * 2 + 1 + (self.cash_desk_standard_zone.cash_desks_number * 2 if self.cash_desk_standard_zone is not None else 0) + 1 + (self.cash_desk_self_service_zone.cash_desks_number * 4 if self.cash_desk_self_service_zone is not None else 0) + self.entering_zone.dimension
        self.grid = SingleGrid(width, height, False)

    def fill_grid(self):
        # Entering zone
        self.entering_zone.build()
        # Shopping zone
        self.shopping_zone.build()
        # Self-scan zone
        self.cash_desk_self_scan_zone.build()
        # Cash-desk standard zone
        self.cash_desk_standard_zone.build()
        # Self-service zone
        self.cash_desk_self_service_zone.build()

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

    def add_occupied_cell(self, direction="", cash_desk_type=CashDeskType.NONE):
        cell = OccupiedCell(len(self.get_occupied_cells()) + 1, self, direction, cash_desk_type)
        self.__occupied_cells.add(cell)
        return cell

    def get_cash_desks(self):
        return self.__cash_desks
