from src.states.State import State
from src.states.CustomerChoosingQueueState import CustomerChoosingQueueState


class CustomerShoppingState(State):

    def action(self):
        if self.context.basket_size < self.context.basket_size_target:
            self.context.shop()
        elif self.context.basket_size_target == self.context.basket_size:
            self.context.state_change(self, CustomerChoosingQueueState(self.context))
