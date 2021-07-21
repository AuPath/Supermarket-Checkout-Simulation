from src.states.State import State
import logging


class CustomerAtCashDeskState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " moving beside the cash desk")

    def get_image(self):
        return "images/pCircle.png"
