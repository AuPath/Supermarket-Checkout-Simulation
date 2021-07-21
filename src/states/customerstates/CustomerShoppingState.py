import logging

from src.states.State import State
from src.states.customerstates.CustomerChoosingQueueState import CustomerChoosingQueueState


class CustomerShoppingState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " is in the SHOPPING ZONE")
        self.context.move_to_shopping_zone()

        self.context.shop()

        if self.context.is_done_shopping():
            self.context.state_change(CustomerChoosingQueueState(self.context))

    def get_image(self):
        if self.context.self_scan:
            return "images/sCircleCyan.png"
        else:
            return "images/sCircleGrey.png"
