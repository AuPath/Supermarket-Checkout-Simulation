from mesa import Agent
from CustomerState import CustomerState


class Customer(Agent):
    """This class represents the client agent."""

    def __init__(self, unique_id, model, basket_size_target, self_scan):
        """Constructor, the basket_size_target and the boolean self_scan are assigned by the main class."""
        super().__init__(unique_id, model)

        self.basket_size = basket_size_target
        self.self_scan = self_scan
        self.state = CustomerState.ENTERED

        self.basket_size_target = 0
        self.target_queue = None
        self.processed_basket = 0

    def step(self):
        if self.state == CustomerState.ENTERED:
            # As the customer enters the market, he waits a step and then starts shopping
            self.state = CustomerState.SHOPPING

        elif self.state == CustomerState.SHOPPING:
            # Every step the customer puts an element in his basket, when he reaches the target basket size, he starts
            # choosing a queue
            if self.basket_size_target > self.basket_size:
                self.basket_size += 1  # TODO: how many items does the customer put in his basket in a step?
            elif self.basket_size_target == self.basket_size:
                self.state = CustomerState.CHOOSING_QUEUE

        elif self.state == CustomerState.CHOOSING_QUEUE:
            # TODO: define the strategy
            pass

        elif self.state == CustomerState.QUEUED:
            # TODO: define the strategy to do jockeying
            pass

        elif self.state == CustomerState.PAYING:
            # TODO: the customer is waiting for some steps and then he exits
            pass

        elif self.state == CustomerState.EXITING:
            # TODO: tell the supermarket to be eliminated
            pass

        else:
            pass

    def choose_queue(self):
        """The customer chooses following a strategy, only if he has already finished to shop."""
        if 0 < self.basket_size == self.basket_size_target and self.basket_size_target > 0:
            pass
        else:
            pass

    def shop(self):
        """The customer enters the shop and starts shopping, he goes on until he has reached the target basket size."""
        if self.basket_size_target > 0:
            pass
        else:
            pass

    def jockey(self):
        """When the customer is following a queue, he can change the queue if he computes that it has less expected
        wait time. """
        if self.target_queue is not None:
            pass
        else:
            pass

    def exit(self):
        """When the customer has finished his payment, he exits the supermarket."""
        pass

    def enter(self):
        """When the customer enters the supermarket, he decises his basket size and if he wants to go to the
        self-scan cash desk. """
        pass
