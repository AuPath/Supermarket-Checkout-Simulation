from src.states.State import State
from src.states.CustomerChoosingQueueState import CustomerChoosingQueueState
import logging


class CustomerShoppingState(State):

    def action(self):

        logging.info("Customer " + str(self.unique_id) + " moves to shopping zone")
        self.context.move_to_shopping_zone()

        self.context.shop()

        if self.context.is_done_shopping():
            self.context.state_change(self, CustomerChoosingQueueState(self.context))
