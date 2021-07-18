from src.states.customerstates import CustomerState
from src.states.customerstates.CustomerShoppingState import CustomerShoppingState
import logging


# State entered when the customer enters the shop
class CustomerEnteredState(CustomerState):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " step")
        self.context.state_change(CustomerShoppingState(self.context))
