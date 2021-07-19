from src.states.State import State
from src.states.customerstates.CustomerShoppingState import CustomerShoppingState
import logging


# State entered when the customer enters the shop
class CustomerEnteredState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " is IN THE STORE")
        logging.info("Customer " + str(self.context.unique_id) + " is moving to the shopping zone")
        self.context.state_change(CustomerShoppingState(self.context))
