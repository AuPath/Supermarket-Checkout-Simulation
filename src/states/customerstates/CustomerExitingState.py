from src.states.customerstates import CustomerState
import logging


class CustomerExitingState(CustomerState):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " exiting")
        self.context.exit_store()
