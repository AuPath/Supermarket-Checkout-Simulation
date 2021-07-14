from src.states.State import State
from src.states.CustomerQueuedState import CustomerQueuedState


class CustomerChoosingQueueState(State):

    def action(self):
        self.context.choose_queue()
        self.context.state_change(CustomerQueuedState(self.context))
