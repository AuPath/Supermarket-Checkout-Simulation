from src.states.State import State
import logging


class CustomerExitingState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " exiting")
        self.context.exit_store()
