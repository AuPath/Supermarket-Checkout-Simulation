from src.states.customerstates import CustomerState
import logging


class CustomerAtCashDeskState(CustomerState):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " moving beside the cash desk")
