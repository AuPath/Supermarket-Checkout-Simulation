from src.states.customerstates import CustomerState
from src.states.customerstates.CustomerQueuedState import CustomerQueuedState
import logging


class CustomerChoosingQueueState(CustomerState):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " choosing queue")

        self.context.target_queue = self.context.choose_queue()
        self.context.target_queue.enqueue(self)

        logging.info("Customer " + str(self.context.unique_id) + " moving to queue")
        self.context.move_to_queue()

        self.context.state_change(CustomerQueuedState(self.context))
