from src.states.State import State
from src.states.CustomerAtCashDeskState import CustomerAtCashDeskState


class CustomerQueuedState(State):

    def action(self):
        self.context.jockey()
        # todo logica del jockeying
