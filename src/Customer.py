import logging

from enums import Enum
from mesa import Agent

SHOPPING_SPEED = 1


class CustomerState(Enum):
    ENTERED = 1
    SHOPPING = 2
    CHOOSING_QUEUE = 3
    QUEUED = 4
    CASH_DESK = 5
    EXITING = 6


class Customer(Agent):
    """This class represents the client agent."""

    def __init__(self, agent_id, model,
                 basket_size_target, self_scan, queue_choice_strategy,
                 shopping_speed=SHOPPING_SPEED):
        """Constructor, the basket_size_target and the boolean self_scan are assigned by the main class."""
        super().__init__(agent_id, model)

        self.type = 0

        self.basket_size = 0
        self.self_scan = self_scan
        self.state = CustomerState.ENTERED

        self.basket_size_target = basket_size_target
        self.target_queue = None
        self.processed_basket = 0

        self.shopping_speed = shopping_speed

        self.queue_choice_strategy = queue_choice_strategy

    def basket_size_target(self):
        return self.basket_size_target

    def increase_processed_basket(self, processing_speed):
        logging.info("Customer " + str(self.unique_id) + " processing basket")
        if self.processed_basket > self.basket_size_target:
            raise Exception("Basket has been already completely processed")
        self.processed_basket += processing_speed

    def step(self):
        logging.info("Customer " + str(self.unique_id) + " step")
        if self.state == CustomerState.ENTERED:
            # As the customer enters the market, he waits a step and then starts shopping, moving in the shopping zone
            self.state = CustomerState.SHOPPING
            logging.info("Customer " + str(self.unique_id) + " moves to shopping zone")
            if not self.model.shopping_zone.is_agent_in_zone(self):
                self.model.shopping_zone.move_to_first_available(self)

        elif self.state == CustomerState.SHOPPING:
            '''
            Every step the customer puts an element i
            n his basket, when
            he reaches the target basket size, he starts choosing a queue
            '''
            if self.basket_size < self.basket_size_target:
                self.shop()
            elif self.basket_size_target == self.basket_size:
                self.state = CustomerState.CHOOSING_QUEUE

        elif self.state == CustomerState.CHOOSING_QUEUE:
            logging.info("Customer " + str(self.unique_id) + " choosing queue")
            self.state = CustomerState.QUEUED
            self.choose_queue()

        elif self.state == CustomerState.QUEUED:
            # TODO: define the strategy to do jockeying
            self.jockey()

    def enter(self):
        """
        When the customer enters the supermarket, he is assigned two variables:
        his basket size and if he wants to go to the self-scan cash desk.
        """
        pass

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

    def choose_queue(self):
        """
        The customer chooses following a strategy,
        only if he has already finished to shop.
        """
        if not self.self_scan:
            self.target_queue = self.queue_choice_strategy.choose_queue(self.model.get_cash_desks(True))
        else:
            self.target_queue = self.model.get_self_scan_queue()
        self.target_queue.enqueue(self)
        logging.info("Customer " + str(self.unique_id) + " moving to queue")
        self.move_to_queue()

    def get_cash_desk(self, queue):
        for cash_desk in self.model.get_cash_desks():
            if cash_desk.queue == queue:
                return cash_desk

    def jockey(self):
        """
        When the customer is following a queue, he can change
        the queue if he computes that it has less expected wait time.
        """
        pass

    def get_state(self):
        return self.state

    def state(self):
        return self.state

    def start_transaction(self):
        self.state = CustomerState.CASH_DESK
        logging.info("Customer " + str(self.unique_id) + " moving beside the cash desk")

    def complete_transaction(self):
        self.state = CustomerState.EXITING
        logging.info("Customer " + str(self.unique_id) + " exiting")
        self.exit_store(self)

    def exit_store(self):
        self.model.remove_customer(self)

    def is_transaction_completed(self):
        return self.basket_size_target <= self.processed_basket

    def advance(self):
        self.model.cash_desk_standard_zone.advance(self)

    def move_to_queue(self):
        cash_desk = self.get_cash_desk(self.target_queue)
        if self.self_scan:
            self.model.cash_desk_self_scan_zone.move_to_queue(self, cash_desk)
        else:
            if type(cash_desk).__name__ == 'CashDeskStandard':
                self.model.cash_desk_standard_zone.move_to_queue(self, cash_desk)
            elif type(cash_desk).__name__ == 'CashDeskSelfService':
                self.model.cash_desk_self_service_zone.move_to_queue(self, cash_desk)
