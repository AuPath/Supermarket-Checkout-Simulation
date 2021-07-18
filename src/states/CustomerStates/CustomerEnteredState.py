from src.states.State import State
from src.states.CustomerStates.CustomerShoppingState import CustomerShoppingState
import logging


# State entered when the customer enters the shop
class CustomerEnteredState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " step")
        self.context.state_change(CustomerShoppingState(self.context))
