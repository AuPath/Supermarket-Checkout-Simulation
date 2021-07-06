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

    def __init__(self, unique_id, model, basket_size_target, self_scan, shopping_speed=SHOPPING_SPEED):
        """Constructor, the basket_size_target and the boolean self_scan are assigned by the main class."""
        super().__init__(unique_id, model)

        self.type = 0

        self.basket_size = basket_size_target
        self.__self_scan = self_scan
        self.__state = CustomerState.ENTERED

        self.__basket_size_target = 0
        self.target_queue = None
        self.processed_basket = 0

        self.__shopping_speed = shopping_speed

    @property
    def basket_size_target(self):
        return self.__basket_size_target

    def increase_processed_basket(self, processing_speed):
        if self.processed_basket > self.__basket_size_target:
            raise Exception("Basket has been already completely processed")
        self.processed_basket += processing_speed

    def step(self):
        if self.__state == CustomerState.ENTERED:
            # As the customer enters the market, he waits a step and then starts shopping
            self.__state = CustomerState.SHOPPING

        elif self.__state == CustomerState.SHOPPING:
            # Every step the customer puts an element in his basket, when he reaches the target basket size, he starts
            # choosing a queue
            self.shop()

        elif self.__state == CustomerState.CHOOSING_QUEUE:
            # TODO: define the strategy
            self.choose_queue()

        elif self.__state == CustomerState.QUEUED:
            # TODO: define the strategy to do jockeying
            self.jockey()

        elif self.__state == CustomerState.CASH_DESK:
            # TODO: the customer is waiting for some steps and then he exits
            pass

        else:
            pass

    def enter(self):
        """When the customer enters the supermarket, he is assigned two variables: his basket size and if he wants to go
        to the self-scan cash desk. """
        pass

    def shop(self):
        """The customer enters the shop and starts shopping, he goes on until he has reached the target basket size."""
        if self.basket_size_target > self.basket_size:
            # TODO: how many items does the customer put in his basket in a step?
            self.basket_size += self.__shopping_speed
        elif self.basket_size_target == self.basket_size:
            self.__state = CustomerState.CHOOSING_QUEUE

    def choose_queue(self):
        """The customer chooses following a strategy, only if he has already finished to shop."""
        pass

    def jockey(self):
        """When the customer is following a queue, he can change the queue if he computes that it has less expected
        wait time. """
        pass

    def get_state(self):
        return self.__state
