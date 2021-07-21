from mesa import Agent

from src.states.State import State
from src.states.customerstates.CustomerEnteredState import CustomerEnteredState

SHOPPING_SPEED = 1


class Customer(Agent):
    """This class represents the client agent."""

    def __init__(self, agent_id, model,
                 basket_size_target, self_scan, queue_choice_strategy,
                 queue_jockeying_strategy,
                 shopping_speed=SHOPPING_SPEED):
        """Constructor, the basket_size_target and the boolean self_scan are assigned by the main class."""
        super().__init__(agent_id, model)

        self.type = 0

        self.basket_size = 0
        self.self_scan = self_scan
        self.state = CustomerEnteredState(self)

        self.basket_size_target = basket_size_target

        # todo Magari target_queue ha piú senso chiamarlo current_queue
        self.target_queue = None

        self.shopping_speed = shopping_speed

        self.queue_choice_strategy = queue_choice_strategy
        self.queue_jockeying_strategy = queue_jockeying_strategy

    def basket_size_target(self):
        return self.basket_size_target

    def step(self):
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
            return self.queue_choice_strategy.choose_queue(self.model.get_working_queues(True))
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
        cash_desk = self.get_cash_desk(self.target_queue)

        chosen_queue = self.queue_jockeying_strategy.switch_queue(self.model.get_adj_cash_desks(cash_desk))
        return chosen_queue

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
            if type(cash_desk).__name__ == 'CashDeskStandard':
                self.model.cash_desk_standard_zone.move_to_queue(self, cash_desk)
            elif type(cash_desk).__name__ == 'CashDeskSelfService':
                self.model.cash_desk_self_service_zone.move_to_queue(self, cash_desk)
