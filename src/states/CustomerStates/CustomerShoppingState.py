from src.states.State import State
from src.states.CustomerStates.CustomerChoosingQueueState import CustomerChoosingQueueState
import logging


class CustomerShoppingState(State):

    def action(self):

        logging.info("Customer " + str(self.context.unique_id) + " moves to shopping zone")
        self.context.move_to_shopping_zone()

        self.context.shop()

        if self.context.is_done_shopping():
            self.context.state_change(CustomerChoosingQueueState(self.context))
