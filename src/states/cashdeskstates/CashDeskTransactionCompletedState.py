from src.states.State import State

from src.states.customerstates.CustomerExitingState import CustomerExitingState
import logging

import typing

if typing.TYPE_CHECKING: # Serve altrimenti ho import circolare
    from src.states.cashdeskstates.CashDeskNewCustomerState import CashDeskNewCustomerState


class CashDeskTransactionCompletedState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        self.context.customer.state_change(CustomerExitingState(self.context.customer))

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskNewCustomerState(self.context))
