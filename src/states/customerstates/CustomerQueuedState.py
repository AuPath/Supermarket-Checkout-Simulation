import logging

from src.states.State import State


class CustomerQueuedState(State):

    def action(self):
        logging.info("Customer " + str(self.context.unique_id) + " is in a QUEUE")

        if not self.context.self_scan:
            chosen_queue = self.context.jockey()

            # Il controllo del None serve nel caso non vogliamo jockeying
            if chosen_queue is not None and chosen_queue != self.context.target_queue:
                self.context.leave_queue() # todo logicamente lo fa nella coda, non so se peró lo bisogna fare anche a livello di cella

                self.context.target_queue = chosen_queue
                self.context.target_queue.enqueue(self.context)
                self.context.move_to_queue() # todo questo svuota la cella in cui era e riempie quella di destinazione ?
