import math
import random

from mesa import Agent

from src.states.State import State
from src.states.customerstates.CustomerEnteredState import CustomerEnteredState

SHOPPING_SPEED = 1
STANDARD_DEVIATION_COEFFICIENT = 0


class Customer(Agent):
    """This class represents the client agent."""

    def __init__(self, agent_id, model,
                 basket_size_target, self_scan, queue_choice_strategy,
                 queue_jockeying_strategy,
                 shopping_speed=SHOPPING_SPEED,
                 standard_deviation_coefficient=STANDARD_DEVIATION_COEFFICIENT):
        """Constructor, the basket_size_target and the boolean self_scan are assigned by the main class."""
        super().__init__(agent_id, model)

        self.type = 0

        self.basket_size = 0
        self.self_scan = self_scan
        self.state = CustomerEnteredState(self)

        self.basket_size_target = basket_size_target

        self.target_queue = None

        self.shopping_speed = shopping_speed

        self.queue_choice_strategy = queue_choice_strategy
        self.queue_jockeying_strategy = queue_jockeying_strategy

        self.standard_deviation_coefficient = standard_deviation_coefficient

        self.waiting_time = 0

    def basket_size_target(self):
        return self.basket_size_target

    def step(self):
        if type(self.state).__name__ == 'CustomerChoosingQueueState' or \
                type(self.state).__name__ == 'CustomerQueuedState':
            self.waiting_time += 1
        self.state.action()

    def shop(self):
        """
        The customer enters the shop and starts shopping,
        he goes on until he has reached the target basket size.
        """

        if self.basket_size + self.shopping_speed >= self.basket_size_target:
            self.basket_size = self.basket_size_target
        else:
            self.basket_size += self.shopping_speed

    def is_done_shopping(self):
        return self.basket_size == self.basket_size_target

    def move_to_shopping_zone(self):
        if not self.model.shopping_zone.is_agent_in_zone(self):
            self.model.shopping_zone.move_to_first_available(self)

    def choose_queue(self):
        """
        The customer chooses a queue based on the the chosen Strategy.
        """
        if not self.self_scan:
            if self.basket_size > 15:
                working_queues = [c for c in self.model.get_working_queues(exclude_self_service=True) if not c.is_queue_full()]
            else:
                working_queues = [c for c in self.model.get_working_queues(exclude_self_service=False) if not c.is_queue_full()]
            if not working_queues:
                return None
            else:
                return self.queue_choice_strategy.choose_queue(working_queues)
        else:
            return self.model.get_self_scan_queue()

    def get_cash_desk(self, queue):
        for cash_desk in self.model.get_cash_desks():
            if cash_desk.queue == queue:
                return cash_desk

    def jockey(self):
        """
        When the customer is following a queue, he can change
        the queue if he computes that it has less expected wait time.
        """

        if self.model.cash_desk_standard_zone is not None:
            cash_desk = self.get_cash_desk(self.target_queue)

        working_adj_cash_desks = self.model.get_adj_cash_desks(cash_desk)
        valid_cash_desks = [c for c in working_adj_cash_desks if not c.is_queue_full()]

        if not valid_cash_desks:
            return None
        else:
            return self.queue_jockeying_strategy.switch_queue(self, working_adj_cash_desks)

    def state(self):
        return self.state

    def state_change(self, new_state: State):
        self.state = new_state

    def exit_store(self):
        self.model.remove_customer(self)

    def advance(self):
        self.model.cash_desk_standard_zone.advance(self)

    def leave_queue(self):
        self.target_queue.remove_element(self)

    def move_to_queue(self):
        cash_desk = self.get_cash_desk(self.target_queue)
        if self.self_scan:
            self.model.cash_desk_self_scan_zone.move_to_queue(self, cash_desk)
        else:
            if cash_desk in self.model.cash_desk_standard_zone.cash_desks:
                if self.model.cash_desk_standard_zone is not None:
                    self.model.cash_desk_standard_zone.move_to_queue(self, cash_desk)
                else:
                    self.model.cash_desk_standard_shared_zone.move_to_queue(self, cash_desk)
            elif cash_desk in self.model.cash_desk_self_service_zone.cash_desks:
                self.model.cash_desk_self_service_zone.move_to_queue(self, cash_desk)

    def estimate_basket_size(self):
        return math.ceil(random.normalvariate(self.basket_size, self.basket_size * self.standard_deviation_coefficient))

    def send_waiting_time(self):
        if not self.self_scan:
            self.model.waiting_times_standard.append(self.waiting_time)
        else:
            self.model.waiting_times_self_scan.append(self.waiting_time)
