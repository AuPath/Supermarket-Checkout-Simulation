from src.states.State import State
from src.states.CustomerShoppingState import CustomerShoppingState


# State entered when the customer enters the shop
class CustomerEnteredState(State):

    def action(self):
        self.context.state_change(CustomerShoppingState(self.context))
