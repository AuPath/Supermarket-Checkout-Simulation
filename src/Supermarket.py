import logging
import math
from statistics import mean
import pickle

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from numpy import random

from src.Customer import Customer
from src.OccupiedCell import OccupiedCell
from src.cashdesk.CashDesk import CashDesk
from src.cashdesk.CashDeskReserved import CashDeskReserved
from src.cashdesk.CashDeskSelfScan import CashDeskSelfScan
from src.cashdesk.CashDeskSelfService import CashDeskSelfService
from src.cashdesk.CashDeskStandard import CashDeskStandard
from src.queue.NormalQueue import NormalQueue
from src.queue.SupermarketQueue import SupermarketQueue
from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy
from src.zones.dinamic.CashDeskReservedZone import CashDeskReservedZone
from src.zones.dinamic.CashDeskSelfScanZone import CashDeskSelfScanZone
from src.zones.dinamic.CashDeskSelfServiceZone import CashDeskSelfServiceZone
from src.zones.dinamic.CashDeskStandardSharedQueueZone import CashDeskStandardSharedQueueZone
from src.zones.dinamic.CashDeskStandardZone import CashDeskStandardZone
from src.zones.stationary.EnteringZone import EnteringZone
from src.zones.stationary.ShoppingZone import ShoppingZone

ADJ_WINDOW_SIZE = 2

GRID_HEIGHT = 20

MAX_CUSTOMER_QUEUED = 6

QUEUED_PERCENTAGE_OPEN_THRESHOLD = 0.6
QUEUED_PERCENTAGE_CLOSE_THRESHOLD = 0.3

# Basket size exponential distribution parameter
LAMBA_EXPONENTIAL_DISTRIBUTION = 0.0736184654254411

SELF_SCAN_PERCENTAGE = 0.4


def generate_basket_size(n, lambda_parameter=LAMBA_EXPONENTIAL_DISTRIBUTION):
    values = map(lambda x: math.ceil(x), random.exponential(scale=1 / lambda_parameter, size=n))
    return list(values)


def generate_customers_metadata(n_customers, queue_choice_strategy: QueueChoiceStrategy,
                                queue_jockey_strategy: QueueJockeyStrategy):
    customers_metadata = []

    basket_size_values = generate_basket_size(n_customers)

    # TODO: che distribuzione hanno i self scan? da inventarsela
    rand_num = random.random()
    for basket_size in basket_size_values:
        self_scan = rand_num < SELF_SCAN_PERCENTAGE
        new_tuple = (basket_size, self_scan, queue_choice_strategy, queue_jockey_strategy)
        customers_metadata.append(new_tuple)
    return customers_metadata


class Supermarket(Model):
    """SuperMARCO model: description here"""

    def __init__(self, zones_metadata, customer_distribution, queue_choice_strategy: QueueChoiceStrategy,
                 queue_jockey_strategy: QueueJockeyStrategy, adj_window_size=ADJ_WINDOW_SIZE):
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
        self.__customer_distribution = customer_distribution
        self.__current_step = 1
        self.__queue_choice_strategy = queue_choice_strategy
        self.__queue_jockey_strategy = queue_jockey_strategy
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
        # Max customer per queue
        self.max_customer_in_queue = MAX_CUSTOMER_QUEUED
        assert self.max_customer_in_queue >= 1

        # TODO: definire qui le metriche
        self.datacollector = DataCollector(
            model_reporters={"Total_customers": self.get_number_of_customers,
                             # grafici fondamentali: densità sull'asse x, flusso sull'asse y
                             # lo facciamo totale e differenziando per tipo di cassa
                             "Density_total": self.get_density_total,
                             # numero di clienti totali fratto numero di casse per ogni step
                             "Flow_total": self.get_flow_total,  # numero di clienti processati per ogni cassa a step,
                             "Density_standard": self.get_density_standard,
                             "Flow_standard": self.get_flow_standard,
                             "Density_self_scan": self.get_density_self_scan,
                             "Flow_self_scan": self.get_flow_self_scan
                             })

    def step(self):
        if self.__current_step < 60 * 8:  # TODO: la giornata finisce dopo 8h
            # continuous creation of customers
            customers_metadata = generate_customers_metadata(self.__customer_distribution[self.__current_step],
                                                             self.__queue_choice_strategy, self.__queue_jockey_strategy)
            self.init_customers(customers_metadata)
            self.__current_step += 1

        # activation / deactivation cash desks
        if self.get_total_customers() > 0:
            while self.need_to_open_cash_desk() and self.get_not_working_queues() != []:
                self.get_not_working_queues()[0].working = True
            else:
                if self.need_to_close_cash_desk():
                    self.get_working_queues(exclude_self_service=True)[-1].working = False
        else:
            self.close_all_cash_desks()

        # Model step
        self.datacollector.collect(self)
        self.customer_scheduler.step()
        self.cash_desk_scheduler.step()

        if self.get_number_of_customers() == 0 and self.__current_step > 1:
            self.dump_data_collector()

    def dump_data_collector(self):
        from datetime import datetime
        timestamp = str(datetime.timestamp(datetime.now())).split('.')[0]
        f_name = f"../pickle/datacollector_{timestamp}.pkl"
        print("ciao")

        with open(f_name, "wb") as f:
            pickle.dump(self.datacollector.model_vars, f)

    def close_all_cash_desks(self):
        for cash_desk in self.get_working_queues():
            cash_desk.working = False

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
            elif zone_type == 'CASH_DESK_STANDARD_SHARED_QUEUE':
                normal_queue = NormalQueue()
                for i in range(dimension):
                    cash_desk = CashDeskStandard(idx, self, normal_queue)
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
        ordered_queues = []
        if self.cash_desk_standard_zone is not None and self.cash_desk_standard_zone.cash_desks_number > 0:
            for cash_desk in self.cash_desk_standard_zone.cash_desks:
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

    def get_working_queues(self, exclude_self_service=False):
        filtered_cash_desk = []
        for cash_desk in self.__cash_desks:
            if cash_desk in self.cash_desk_self_service_zone.cash_desks and not exclude_self_service:
                filtered_cash_desk.append(cash_desk)
            elif cash_desk in self.cash_desk_standard_zone.cash_desks and cash_desk.working:
                filtered_cash_desk.append(cash_desk)
        return filtered_cash_desk

    def get_not_working_queues(self):
        filtered_cash_desk = []
        for cash_desk in self.__cash_desks:
            if cash_desk in self.cash_desk_standard_zone.cash_desks and not cash_desk.working:
                filtered_cash_desk.append(cash_desk)
        return filtered_cash_desk

    def need_to_open_cash_desk(self, opening_threshold=QUEUED_PERCENTAGE_OPEN_THRESHOLD):
        if len(self.get_working_queues(exclude_self_service=True)) == 0:
            return True
        if self.avg_queue_load() > opening_threshold:
            return True
        else:
            return False

    def need_to_close_cash_desk(self, closing_threshold=QUEUED_PERCENTAGE_CLOSE_THRESHOLD):
        if len(self.get_working_queues(exclude_self_service=True)) == 1:
            return False
        if self.avg_queue_load() < closing_threshold:
            return True
        else:
            return False

    def avg_queue_load(self):
        avg_load = mean(map(lambda x: x.queue.size(), self.get_working_queues(exclude_self_service=True)))
        return avg_load / MAX_CUSTOMER_QUEUED

    def get_total_customers(self):
        # questo metodo serve per l'attivazione e la disattivazione delle casse
        # ritorna i clienti che devono essere ancora processati e che sono presenti nel supermarket:
        # ovvero i clienti negli stati CustomerEnteredState, CustomerShoppingState, CustomerChoosingQueueState e
        # CustomerQueuedState -> tutto tranne CustomerAtCashDeskState
        total_customers = 0
        for customer in self.__customers:
            if type(customer.state).__name__ != 'CustomerAtCashDeskState':
                total_customers += 1

        return total_customers

    def get_number_of_customers(self, exclude_self_scan=False):
        if exclude_self_scan:
            n_customers = 0
            for customer in self.__customers:
                if not customer.self_scan:
                    n_customers += 1
            return n_customers
        else:
            return len(self.__customers)

    def get_number_processed_customers(self, exclude_self_scan=False):
        n = 0
        if exclude_self_scan:
            cash_desks = self.get_cash_desks(exclude_self_scan=True)
        else:
            cash_desks = self.get_cash_desks()

        for cash_desk in cash_desks:
            cash_desk_type = type(cash_desk.state).__name__
            if cash_desk_type == 'CashDeskStandardTransactionCompletedState' or \
                    cash_desk_type == 'CashDeskSelfServiceTransactionCompletedState' or \
                    cash_desk_type == 'CashDeskSelfScanTransactionCompletedState' or \
                    cash_desk_type == 'CashDeskReservedTransactionCompletedState':
                n += 1

        return n

    def get_density_total(self):
        # numero di clienti totale / numero di casse totali
        return self.get_number_of_customers() / len(self.get_cash_desks())

    def get_flow_total(self):
        # numero di clienti processati (uscenti) totali
        return self.get_number_processed_customers() / len(self.get_cash_desks())

    def get_density_standard(self):
        # numero di clienti non self scan / numero di casse non self scan
        return self.get_number_of_customers(exclude_self_scan=True) / len(self.get_cash_desks(exclude_self_scan=True))

    def get_flow_standard(self):
        # numero di clienti processati (uscenti) dalle casse non self scan
        return self.get_number_processed_customers(exclude_self_scan=True) / \
               len(self.get_cash_desks(exclude_self_scan=True))

    def get_density_self_scan(self):
        # numero di clienti self scan / numero di casse self scan
        return (self.get_number_of_customers() - self.get_number_of_customers(exclude_self_scan=True)) / \
               len(self.get_cash_desks_by_type("CashDeskSelfScan"))

    def get_flow_self_scan(self):
        # numero di clienti processati (uscenti) dalle casse self scan
        return (self.get_number_processed_customers() - self.get_number_processed_customers(exclude_self_scan=True)) / \
               len(self.get_cash_desks_by_type("CashDeskSelfScan"))

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
                if cash_desk in self.cash_desk_self_scan_zone.cash_desks:
                    filtered_cash_desk.append(cash_desk)
            return filtered_cash_desk
