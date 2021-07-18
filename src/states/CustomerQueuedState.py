from src.states.State import State
from src.states.CustomerAtCashDeskState import CustomerAtCashDeskState


class CustomerQueuedState(State):

    def action(self):
        chosen_queue = self.context.jockey()

        # Il controllo del None serve nel caso non vogliamo jockeying
        if chosen_queue is not None and chosen_queue != self.context.target_queue:
            self.context.target_queue = chosen_queue
            self.context.target_queue.enqueue(self)