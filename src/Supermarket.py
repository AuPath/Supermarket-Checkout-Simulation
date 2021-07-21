import logging
import random

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from src.Customer import Customer
from src.OccupiedCell import OccupiedCell
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
from src.zones.dinamic.CashDeskStandardSharedQueueZone import CashDeskStandardSharedQueueZone
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
        self.cash_desk_standard_shared_zone = None
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
        # logging.info("Step")

        while self.is_active_cash_desk_needed():
            if len(self.get_not_working_queues()) > 0:
                if self.is_active_cash_desk_needed():
                    self.get_not_working_queues()[0].working = True
                else:
                    self.get_not_working_queues()[0].working = False

        self.customer_scheduler.step()
        self.cash_desk_scheduler.step()

    def init_customers(self, customers_metadata):
        logging.info("Init customers")
        for basket_size, self_scan, queue_choice_strategy, queue_jockey_strategy in customers_metadata:
            customer = Customer(self.__num_agent, self, basket_size, self_scan, queue_choice_strategy,
                                queue_jockey_strategy)
            self.__num_agent += 1
            self.add_customer(customer)

    def init_zones(self):
        logging.info("Init zones")
        for zone_type, dimension in self.zones_metadata:
            if zone_type == 'ENTERING':
                self.entering_zone = EnteringZone(self, dimension)
            elif zone_type == 'SHOPPING':
                self.shopping_zone = ShoppingZone(self, dimension)
            elif zone_type == 'CASH_DESK_STANDARD':
                self.cash_desk_standard_zone = CashDeskStandardZone(self, dimension)
            elif zone_type == 'CASH_DESK_STANDARD_SHARED_QUEUE':
                self.cash_desk_standard_shared_zone = CashDeskStandardSharedQueueZone(self, dimension)
            elif zone_type == 'CASH_DESK_SELF_SERVICE':
                self.cash_desk_self_service_zone = CashDeskSelfServiceZone(self, dimension)
            elif zone_type == 'CASH_DESK_SELF_SCAN':
                self.cash_desk_self_scan_zone = CashDeskSelfScanZone(self, dimension)
            elif zone_type == 'CASH_DESK_RESERVED':
                self.cash_desk_reserved_zone = CashDeskReservedZone(self, dimension)
            else:
                pass

    def init_cash_desks(self):
        logging.info("Init cash desks")
        idx = 1
        for zone_type, dimension in self.zones_metadata:
            if zone_type == 'CASH_DESK_STANDARD':
                for i in range(dimension):
                    cash_desk = CashDeskStandard(idx, self, NormalQueue())
                    self.cash_desk_standard_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
                # TODO: quante casse devono essere aperte sempre? ne metto 2
                if self.get_cash_desk_by_id(1):
                    self.get_cash_desk_by_id(1).working = True
                if self.get_cash_desk_by_id(2):
                    self.get_cash_desk_by_id(2).working = True
            elif zone_type == 'CASH_DESK_STANDARD_SHARED_QUEUE':
                normal_queue = NormalQueue()
                for i in range(dimension):
                    cash_desk = CashDeskStandard(idx, self, normal_queue, True)
                    self.cash_desk_standard_shared_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
            elif zone_type == 'CASH_DESK_SELF_SERVICE':
                for i in range(dimension):
                    normal_queue = NormalQueue()
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
                    self.add_cash_desk_to_self_service_zone(idx, normal_queue)
                    idx += 1
            elif zone_type == 'CASH_DESK_SELF_SCAN':
                normal_queue = NormalQueue()
                for i in range(dimension):
                    cash_desk = CashDeskSelfScan(idx, self, normal_queue)
                    self.cash_desk_self_scan_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1
            elif zone_type == 'CASH_DESK_RESERVED':
                if self.cash_desk_self_scan_zone is not None and self.cash_desk_self_scan_zone.cash_desks_number > 0:
                    cash_desk = CashDeskReserved(idx, self, NormalQueue())
                    self.cash_desk_reserved_zone.cash_desks.append(cash_desk)
                    self.add_cash_desk(cash_desk)
                    idx += 1

    def add_cash_desk_to_self_service_zone(self, idx, normal_queue):
        cash_desk = CashDeskSelfService(idx, self, normal_queue)
        self.cash_desk_self_service_zone.cash_desks.append(cash_desk)
        self.add_cash_desk(cash_desk)

    def init_environment(self):
        logging.info("Init environment")
        # Build grid
        self.init_grid()
        # Fill grid
        self.fill_grid()

    def init_grid(self):
        logging.info("Init grid")
        height = GRID_HEIGHT
        width = (
                    self.cash_desk_self_scan_zone.cash_desks_number * 2 if self.cash_desk_self_scan_zone is not None else 0) \
                + 3 + (
                    self.cash_desk_standard_zone.cash_desks_number * 2 if self.cash_desk_standard_zone is not None else 0) \
                + (
                    self.cash_desk_standard_shared_zone.cash_desks_number * 2 if self.cash_desk_standard_shared_zone is not None else 0) \
                + 1 + (
                    self.cash_desk_self_service_zone.cash_desks_number * 8 if self.cash_desk_self_service_zone is not None else 0) \
                + 1 + self.entering_zone.dimension
        self.grid = SingleGrid(width, height, False)

    def fill_grid(self):
        logging.info("Fill grid")
        # Entering zone
        self.entering_zone.build()
        # Shopping zone
        self.shopping_zone.build()
        # Self-scan zone
        self.cash_desk_self_scan_zone.build()
        # Reserved zone
        self.cash_desk_reserved_zone.build()
        # Cash-desk standard zone
        if self.cash_desk_standard_zone is not None:
            self.cash_desk_standard_zone.build()
        # Cash-desk standard zone with shared queue
        if self.cash_desk_standard_shared_zone is not None:
            self.cash_desk_standard_shared_zone.build()
        # Self-service zone
        self.cash_desk_self_service_zone.build()

    def add_cash_desk(self, cash_desks):
        self.__cash_desks.append(cash_desks)
        self.cash_desk_scheduler.add(cash_desks)

    def add_customer(self, customer: Customer):
        self.__customers.add(customer)
        self.customer_scheduler.add(customer)

        # Add the agent to the entering zone of the market
        position = self.find_empty_entering_cell()
        self.grid.place_agent(customer, position)
        return

    def find_empty_entering_cell(self):
        empties = self.grid.empties
        filtered_empties = []
        for empty in empties:
            if empty[0] > self.grid.width - self.entering_zone.dimension \
                    and empty[1] < self.grid.height - self.shopping_zone.dimension:
                filtered_empties.append(empty)
        return filtered_empties[random.randint(0, len(filtered_empties) - 1)]

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

    def get_self_scan_queue(self):
        if self.cash_desk_self_scan_zone.cash_desks is not None and len(self.cash_desk_self_scan_zone.cash_desks) > 0:
            return self.cash_desk_self_scan_zone.cash_desks[0].queue
        else:
            return None

    def get_unique_queues(self):
        return set(self.queues)

    # returns the adjacent queues to the given queue
    def get_adj_cash_desks(self, pivot_cash_desk: CashDesk):
        # TODO: ricontrollare, penso sia giusto così perchè per le self-service vanno ritornate tutte e 4
        # todo ritorna lista vuota
        # le casse del gruppo. Per come era prima non teneva conto delle altre 3 casse invece deve, perchè
        # se una è vuota deve andare lì e non ad esempio in una cassa normale dove c'è un cliente che paga
        # list of queues in the right order
        ordered_queues = []
        if self.cash_desk_standard_zone is not None and self.cash_desk_standard_zone.cash_desks_number > 0:
            for cash_desk in self.cash_desk_standard_zone.cash_desks:
                # already ordered
                if cash_desk.queue not in ordered_queues:
                    ordered_queues.append(cash_desk.queue)
        if self.cash_desk_self_service_zone is not None and self.cash_desk_self_service_zone.cash_desks_number > 0:
            for cash_desk in self.cash_desk_self_service_zone.cash_desks:
                # already ordered
                if cash_desk.queue not in ordered_queues:
                    ordered_queues.append(cash_desk.queue)

        chosen_queue_index = ordered_queues.index(pivot_cash_desk.queue)

        left_queues = ordered_queues[max(0, chosen_queue_index - ADJ_WINDOW_SIZE):chosen_queue_index]
        right_queues = ordered_queues[chosen_queue_index + 1:chosen_queue_index + ADJ_WINDOW_SIZE + 1]

        # adjacent_queues = left_queues + [pivot_cash_desk.queue] + right_queues
        adjacent_queues = left_queues + right_queues

        adjacent_cash_desks = []
        for queue in adjacent_queues:
            adjacent_cash_desks = adjacent_cash_desks + self.get_cash_desks_by_queue(queue)

        adjacent_cash_desks = list(filter(lambda x: x.working, adjacent_cash_desks))
        return adjacent_cash_desks

    def get_cash_desks_by_queue(self, queue: SupermarketQueue):
        cash_desks = []
        for cash_desk in self.get_cash_desks():
            if cash_desk.queue == queue:
                cash_desks.append(cash_desk)

        return cash_desks

    def get_cash_desks_by_type(self, cash_desk_type):
        cash_desks = []
        for cash_desk in self.get_cash_desks():
            if type(cash_desk).__name__ == cash_desk_type:
                cash_desks.append(cash_desk)

        return cash_desks

    def get_cash_desk_by_id(self, unique_id):
        for cash_desk in self.get_cash_desks():
            if cash_desk.unique_id == unique_id:
                return cash_desk

    def get_working_queues(self):
        filtered_cash_desk = []
        for cash_desk in self.__cash_desks:
            if type(cash_desk).__name__ == "CashDeskSelfService":
                filtered_cash_desk.append(cash_desk)
            elif type(cash_desk).__name__ == "CashDeskStandard" and cash_desk.working:
                filtered_cash_desk.append(cash_desk)
        return filtered_cash_desk

    def get_not_working_queues(self):
        filtered_cash_desk = []
        for cash_desk in self.__cash_desks:
            if type(cash_desk).__name__ == "CashDeskStandard" and not cash_desk.working:
                filtered_cash_desk.append(cash_desk)
        return filtered_cash_desk

    def is_active_cash_desk_needed(self):
        if len(self.get_working_queues()) <= 2:
            return True
        else:
            if self.get_total_customers() > len(self.get_working_queues()) * 5:
                return True
            else:
                return False

    def get_total_customers(self):
        # questo metodo serve per l'attivazione e la disattivazione delle casse
        # ritorna i clienti che devono essere ancora processati e che sono presenti nel supermarket:
        # ovvero i clienti negli stati CustomerEnteredState, CustomerShoppingState, CustomerChoosingQueueState e
        # CustomerQueuedState -> tutto tranne CustomerAtCashDeskState
        total_customers = 0
        for customer in self.__customers:
            if type(customer.state).__name__ != 'CustomeAtCashDeskState':
                total_customers += 1

        return total_customers

    def get_occupied_cells(self):
        return self.__occupied_cells

    def add_occupied_cell(self, direction):
        cell = OccupiedCell(len(self.get_occupied_cells()) + 1, self, direction)
        self.__occupied_cells.add(cell)
        return cell

    def get_cash_desks(self, exclude_self_scan=False):
        if not exclude_self_scan:
            return self.__cash_desks
        else:
            filtered_cash_desk = []
            for cash_desk in self.__cash_desks:
                if not type(cash_desk).__name__ == "CashDeskSelfScan":
                    filtered_cash_desk.append(cash_desk)
            return filtered_cash_desk
