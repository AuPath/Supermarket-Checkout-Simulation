from src.states.State import State
from src.states.customerstates.CustomerQueuedState import CustomerQueuedState
import logging


class CustomerChoosingQueueState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " choosing queue")

        self.context.target_queue = self.context.choose_queue()

        if self.context.target_queue is not None:
            self.context.target_queue.enqueue(self.context)

            logging.info("Customer " + str(self.context.unique_id) + " moving to a queue")
            self.context.move_to_queue()

            self.context.state_change(CustomerQueuedState(self.context))

    def get_image(self):
        return "images/cCircle.png"
