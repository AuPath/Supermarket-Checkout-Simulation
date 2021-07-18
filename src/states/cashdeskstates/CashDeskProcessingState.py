from src.states.State import State
from src.states.cashdeskstates.CashDeskTransactionCompletedState import CashDeskTransactionCompletedState
import logging


class CashDeskProcessingState(State):

    def action(self):
        logging.info("Cash desk " + type(self).__name__ + " " + str(self.context.unique_id) +
                     " processing customer " + str(self.context.customer.unique_id))

        self.context.process_customer()

        if self.context.is_transaction_complete():
            self.context.state_change(CashDeskTransactionCompletedState(self.context))
