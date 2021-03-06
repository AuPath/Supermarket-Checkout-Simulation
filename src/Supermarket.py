import logging
import math
import pickle
from os.path import join
from statistics import mean

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
from src.config import PICKLE_PATH
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
MAX_CUSTOMER_QUEUED = 10

QUEUED_PERCENTAGE_OPEN_THRESHOLD = 0.5
QUEUED_PERCENTAGE_CLOSE_THRESHOLD = 0.3

# Basket size exponential distribution parameter
LAMBDA_EXPONENTIAL_DISTRIBUTION = 0.0736184654254411


def generate_basket_size(n, lambda_parameter=LAMBDA_EXPONENTIAL_DISTRIBUTION):
    values = map(lambda x: math.ceil(x), random.exponential(scale=1 / lambda_parameter, size=n))
    return list(values)


class Supermarket(Model):
    """Supermarket model: agent based model to simulate the behavior of customers in the supermarket"""

    def __init__(self, zones_metadata, customer_distribution, grid_height,
                 queue_choice_strategy: QueueChoiceStrategy, queue_jockey_strategy: QueueJockeyStrategy,
                 simulation_name, customer_shopping_speed, period_in_seconds,
                 customer_standard_deviation_coefficient=0,
                 self_scan_percentage=0.4, adj_window_size=ADJ_WINDOW_SIZE):
        self.__customers = set()
        self.__occupied_cells = set()
        self.__cash_desks: list[CashDesk] = []
        self.grid = None
        self.grid_height = grid_height
        self.customer_scheduler = RandomActivation(self)
        self.cash_desk_scheduler = RandomActivation(self)
        self.__adj_window_size = adj_window_size
        self.__num_agent = 0
        self.running = True
        self.queues = None
        self.has_shared_queue = False
        self.customer_distribution = customer_distribution
        self.current_step = 1
        self.__queue_choice_strategy = queue_choice_strategy
        self.__queue_jockey_strategy = queue_jockey_strategy
        self.zones_metadata = zones_metadata
        # Simulation name
        self.simulation_name = simulation_name
        # Time parameters
        self.customer_shopping_speed = customer_shopping_speed
        self.period_in_seconds = period_in_seconds
        # Customer standard deviation error
        self.customer_standard_deviation_coefficient = customer_standard_deviation_coefficient
        # Customers distribution
        self.self_scan_percentage = self_scan_percentage
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

        self.__waiting_times_standard = []
        self.__waiting_times_self_scan = []

        self.datacollector = DataCollector(
            model_reporters={"Total_customers": self.get_number_of_customers,
                             # grafici fondamentali: densit?? sull'asse x, flusso sull'asse y
                             # lo facciamo totale e differenziando per tipo di cassa
                             "Density_total": self.get_density_total,
                             # numero di clienti totali fratto numero di casse per ogni step
                             "Flow_total": self.get_flow_total,  # numero di clienti processati per ogni cassa a step,
                             "Density_standard": self.get_density_standard,
                             "Flow_standard": self.get_flow_standard,
                             "Density_self_scan": self.get_density_self_scan,
                             "Flow_self_scan": self.get_flow_self_scan,
                             "Total_steps": self.get_current_step,
                             "Avg_waiting_times_standard": self.get_avg_waiting_times_standard,
                             "Avg_waiting_times_self_scan": self.get_avg_waiting_times_self_scan,
                             "Number_exiting_customers": self.get_number_exiting_customers
                             })

    def step(self):
        if self.current_step < len(self.customer_distribution):
            # continuous creation of customers
            customers_metadata = self.generate_customers_metadata()
            self.init_customers(customers_metadata)
            self.current_step += 1

        # activation / deactivation cash desks
        if self.get_total_customers() > 0:
            if (not self.has_shared_queue
                    and (self.cash_desk_standard_zone is not None
                         or self.cash_desk_standard_shared_zone is not None)):
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

        if self.get_number_of_customers() == 0 and self.current_step >= len(self.customer_distribution):
            self.stop_simulation()

    def generate_customers_metadata(self):
        n_customers = self.customer_distribution[self.current_step]
        customers_metadata = []

        basket_size_values = generate_basket_size(n_customers)

        for basket_size in basket_size_values:
            self_scan = random.random() < self.self_scan_percentage
            new_tuple = (basket_size, self_scan, self.__queue_choice_strategy, self.__queue_jockey_strategy)
            customers_metadata.append(new_tuple)
        return customers_metadata

    def stop_simulation(self):
        self.dump_data_collector()
        self.running = False

    def dump_data_collector(self):
        from datetime import datetime
        timestamp = str(datetime.timestamp(datetime.now())).split('.')[0]
        f_name = join(PICKLE_PATH, f"datacollector${self.simulation_name}${timestamp}.pkl")
        print("Dump data collector completed")

        with open(f_name, "wb") as f:
            pickle.dump(self.datacollector.model_vars, f)

    def close_all_cash_desks(self):
        for cash_desk in self.get_working_queues():
            cash_desk.working = False

    def init_customers(self, customers_metadata):
        logging.info("Init customers")
        for basket_size, self_scan, queue_choice_strategy, queue_jockey_strategy in customers_metadata:
            customer = Customer(self.__num_agent, self, basket_size, self_scan, queue_choice_strategy,
                                queue_jockey_strategy, shopping_speed=self.customer_shopping_speed,
                                standard_deviation_coefficient=self.customer_standard_deviation_coefficient)
            self.__num_agent += 1
            self.add_customer(customer)

    def init_zones(self):
        logging.info("Init zones")
        for zone_type, dimension in self.zones_metadata:
            if dimension == 0:
                pass
            elif zone_type == 'ENTERING':
                self.entering_zone = EnteringZone(self, dimension)
            elif zone_type == 'SHOPPING':
                self.shopping_zone = ShoppingZone(self, dimension)
            elif zone_type == 'CASH_DESK_STANDARD':
                self.cash_desk_standard_zone = CashDeskStandardZone(self, dimension)
            elif zone_type == 'CASH_DESK_STANDARD_SHARED_QUEUE':
                self.cash_desk_standard_shared_zone = CashDeskStandardSharedQueueZone(self, dimension)
                self.has_shared_queue = True
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
        estimation_bias = True if self.customer_standard_deviation_coefficient > 0 else False
        for zone_type, dimension in self.zones_metadata:
            if dimension == 0:
                pass
            elif zone_type == 'CASH_DESK_STANDARD':
                for i in range(dimension):
                    cash_desk = CashDeskStandard(idx, self, NormalQueue(), estimation_bias=estimation_bias)
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
        height = self.grid_height
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
        if self.cash_desk_self_scan_zone is not None:
            self.cash_desk_self_scan_zone.build()
        # Reserved zone
        if self.cash_desk_reserved_zone is not None:
            self.cash_desk_reserved_zone.build()
        # Cash-desk standard zone
        if self.cash_desk_standard_zone is not None:
            self.cash_desk_standard_zone.build()
        # Cash-desk standard zone with shared queue
        if self.cash_desk_standard_shared_zone is not None:
            self.cash_desk_standard_shared_zone.build()
        # Self-service zone
        if self.cash_desk_self_service_zone is not None:
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
            if (self.cash_desk_self_service_zone is not None
                    and cash_desk in self.cash_desk_self_service_zone.cash_desks
                    and not exclude_self_service):
                filtered_cash_desk.append(cash_desk)
            elif (self.cash_desk_standard_zone is not None
                  and cash_desk in self.cash_desk_standard_zone.cash_desks
                  and cash_desk.working):
                filtered_cash_desk.append(cash_desk)
            elif (self.cash_desk_standard_shared_zone is not None
                  and cash_desk in self.cash_desk_standard_shared_zone.cash_desks
                  and cash_desk.working):
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
        data_points = list(map(lambda x: x.queue.size(), self.get_working_queues(exclude_self_service=True)))
        if data_points:
            return mean(data_points) / MAX_CUSTOMER_QUEUED
        else:
            return 0

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

    def get_number_entering_customers(self, exclude_self_scan=False):
        n = 0
        for customer in self.__customers:
            if type(customer.state).__name__ == 'CustomerEnteredState':
                if exclude_self_scan:
                    if not customer.self_scan:
                        n += 1
                else:
                    n += 1

        return n

    def get_number_exiting_customers(self, exclude_self_scan=False):
        n = 0
        for cashdesk in self.__cash_desks:
            if type(cashdesk.state).__name__ == 'CashDeskStandardTransactionCompletedState':
                if exclude_self_scan:
                    if not type(cashdesk).__name__ == 'CashDeskSelfScan':
                        n += 1
                else:
                    n += 1

        return n

    def get_density_total(self):
        # numero di clienti totale / numero di casse totali
        return self.get_number_of_customers() / len(self.get_number_working_cash_desks(exclude_self_scan=False))

    def get_flow_total(self):
        # numero di clienti entranti totali
        return self.get_number_entering_customers() / len(self.get_number_working_cash_desks(exclude_self_scan=False))

    def get_density_standard(self):
        # numero di clienti non self scan / numero di casse non self scan
        n_cash_desks = len(self.get_number_working_cash_desks(exclude_self_scan=True))
        if n_cash_desks == 0:
            return 0
        else:
            return self.get_number_of_customers(exclude_self_scan=True) / n_cash_desks

    def get_flow_standard(self):
        # numero di clienti entranti non self scan
        n_cash_desks = len(self.get_number_working_cash_desks(exclude_self_scan=False))
        if n_cash_desks == 0:
            return 0
        else:
            return self.get_number_entering_customers(exclude_self_scan=True) / n_cash_desks

    def get_density_self_scan(self):
        # numero di clienti self scan / numero di casse self scan

        if len(self.get_cash_desks_by_type("CashDeskSelfScan")) == 0:
            return 0
        else:
            return (self.get_number_of_customers() - self.get_number_of_customers(exclude_self_scan=True)) / \
                   len(self.get_cash_desks_by_type("CashDeskSelfScan"))

    def get_flow_self_scan(self):
        # numero di clienti entranti self scan

        if len(self.get_cash_desks_by_type("CashDeskSelfScan")) == 0:
            return 0
        else:
            return (self.get_number_entering_customers() - self.get_number_entering_customers(exclude_self_scan=True)) / \
                   len(self.get_cash_desks_by_type("CashDeskSelfScan"))

    def get_current_step(self):
        return self.current_step

    @property
    def waiting_times_standard(self):
        return self.__waiting_times_standard

    @waiting_times_standard.setter
    def waiting_times_standard(self, value):
        self.__waiting_times_standard = value

    @property
    def waiting_times_self_scan(self):
        return self.__waiting_times_self_scan

    @waiting_times_self_scan.setter
    def waiting_times_self_scan(self, value):
        self.__waiting_times_self_scan = value

    def get_avg_waiting_times_standard(self):
        if len(self.__waiting_times_standard) != 0:
            return sum(self.__waiting_times_standard) / len(self.__waiting_times_standard)
        else:
            return 0

    def get_avg_waiting_times_self_scan(self):
        if len(self.__waiting_times_self_scan) != 0:
            return sum(self.__waiting_times_self_scan) / len(self.__waiting_times_self_scan)
        else:
            return 0

    def get_occupied_cells(self):
        return self.__occupied_cells

    def add_occupied_cell(self, direction):
        cell = OccupiedCell(len(self.get_occupied_cells()) + 1, self, direction)
        self.__occupied_cells.add(cell)
        return cell

    def get_cash_desks(self, exclude_self_scan=False):
        if not exclude_self_scan or self.cash_desk_self_scan_zone is None:
            return self.__cash_desks
        else:
            filtered_cash_desk = []
            for cash_desk in self.__cash_desks:
                if cash_desk not in self.cash_desk_self_scan_zone.cash_desks:
                    filtered_cash_desk.append(cash_desk)
            return filtered_cash_desk

    def get_number_working_cash_desks(self, exclude_self_scan=False):
        if not exclude_self_scan or self.cash_desk_self_scan_zone is None:
            filtered_cash_desks = []
            for cash_desk in self.__cash_desks:
                if ((self.cash_desk_standard_zone is not None and cash_desk in self.cash_desk_standard_zone.cash_desks and cash_desk.working) or
                    (self.cash_desk_self_service_zone is not None and cash_desk in self.cash_desk_self_service_zone.cash_desks) or
                    (self.cash_desk_self_scan_zone is not None and cash_desk in self.cash_desk_self_scan_zone.cash_desks)):
                    filtered_cash_desks.append(cash_desk)
            return filtered_cash_desks
        else:
            filtered_cash_desks = []
            for cash_desk in self.__cash_desks:
                if ((self.cash_desk_standard_zone is not None and cash_desk in self.cash_desk_standard_zone.cash_desks and cash_desk.working) or
                        (self.cash_desk_self_service_zone is not None and cash_desk in self.cash_desk_self_service_zone.cash_desks)):
                    filtered_cash_desks.append(cash_desk)
            return filtered_cash_desks
