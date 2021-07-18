from src.states.cashdeskstates.CashDeskState import CashDeskState
from src.states.cashdeskstates.CashDeskProcessingState import CashDeskProcessingState
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState
import logging


class CashDeskNewCustomerState(CashDeskState):

    def action(self):
        if self.context.queue.size() > 0:

            # Prendo il cliente e gli cambio lo stato
            self.context.customer = self.context.queue.dequeue()
            self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

            self.context.move_beside(self.context.customer)

            for customer in self.context.queue.content():
                self.context.advance(customer)

            self.context.state_change(CashDeskProcessingState(self.context))
