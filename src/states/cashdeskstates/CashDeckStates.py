from src.states.State import State
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState
from src.states.customerstates.CustomerExitingState import CustomerExitingState
import logging


class CashDeskNewCustomerState(State):

    def action(self):
        if self.context.queue.size() > 0:

            # Prendo il cliente e gli cambio lo stato
            self.context.customer = self.context.queue.dequeue()
            self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

            self.context.move_beside()

            for customer in self.context.queue.content():
                self.context.advance(customer)

            self.context.state_change(CashDeskProcessingState(self.context))


class CashDeskProcessingState(State):

    def action(self):
        logging.info("Cash desk " + type(self).__name__ + " " + str(self.context.unique_id) +
                     " processing customer " + str(self.context.customer.unique_id))

        self.context.process_customer()

        if self.context.is_transaction_complete():
            self.context.state_change(CashDeskTransactionCompletedState(self.context))


class CashDeskTransactionCompletedState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        self.context.customer.state_change(CustomerExitingState(self.context.customer))

        # terminato un cliente riprendo ad accettarne di nuovi
        # TODO: durante l'esecuzione ricevo l'errore name 'CashDeskNewCustomerState' is not defined
        # ha a che fare con l'import sopra, come sistemare?
        self.context.state_change(CashDeskNewCustomerState(self.context))
