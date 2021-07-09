from mesa import Agent
from enums import Enum

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
        if self.processed_basket > self.basket_size_target:
            raise Exception("Basket has been already completely processed")
        self.processed_basket += processing_speed

    def step(self):
        if self.state == CustomerState.ENTERED:
            # As the customer enters the market, he waits a step and then starts shopping
            self.state = CustomerState.SHOPPING

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
            # TODO: define the strategy
            self.choose_queue()
            self.state = CustomerState.QUEUED

        elif self.state == CustomerState.QUEUED:
            # TODO: define the strategy to do jockeying
            self.jockey()

        elif self.state == CustomerState.CASH_DESK:
            # TODO: the customer is waiting for some steps and then he exits
            pass

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
        self.basket_size += self.shopping_speed

    def choose_queue(self):
        """
        The customer chooses following a strategy,
        only if he has already finished to shop.
        """
        all_queues = self.model.queues
        self.target_queue = self.queue_choice_strategy.choose_queue(all_queues)
        self.target_queue.enqueue(self)

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

    def complete_transaction(self):
        self.state = CustomerState.EXITING

    def transaction_is_completed(self):
        return self.basket_size_target <= self.processed_basket


