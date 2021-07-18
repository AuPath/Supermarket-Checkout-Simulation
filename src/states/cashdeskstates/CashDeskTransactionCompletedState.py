from src.states.cashdeskstates.CashDeskState import CashDeskState
from src.states.cashdeskstates.CashDeskNewCustomerState import CashDeskNewCustomerState
from src.states.customerstates.CustomerExitingState import CustomerExitingState
import logging


class CashDeskTransactionCompletedState(CashDeskState):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        self.context.customer.state_change(CustomerExitingState(self.context.customer))

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskNewCustomerState(self.context))
