from src.states.State import State
import logging


class CustomerQueuedState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " is queued")

        chosen_queue = self.context.jockey()

        # Il controllo del None serve nel caso non vogliamo jockeying
        if chosen_queue is not None and chosen_queue != self.context.target_queue:
            self.context.target_queue = chosen_queue
            self.context.target_queue.enqueue(self)