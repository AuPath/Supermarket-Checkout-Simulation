import logging

from src.states.State import State
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState


class CashDeskStandardNewCustomerState(State):

    def action(self):
        if self.context.queue.size() > 0:

            # Prendo il cliente e gli cambio lo stato
            self.context.customer = self.context.queue.dequeue()

            logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                         " has acquired customer " + str(self.context.customer.unique_id))

            self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

            self.context.move_customer_beside_cashdesk()

            self.context.state_change(CashDeskStandardProcessingState(self.context))

            if self.context.queue.size() > 0:
                for customer in self.context.queue.content():
                    self.context.advance(customer)


class CashDeskStandardProcessingState(State):

    def action(self):
        if self.context.working or self.context.customer is not None:
            logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                         " processing customer " + str(self.context.customer.unique_id))

            self.context.process_customer()

            if self.context.is_transaction_complete():
                self.context.customer.exit_store()

                logging.info("Customer exited")
                self.context.state_change(CashDeskStandardTransactionCompletedState(self.context))


class CashDeskStandardTransactionCompletedState(State):

    def action(self):
        if self.context.working:
            logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                         " completing the transaction")

            # terminato un cliente riprendo ad accettarne di nuovi
            self.context.state_change(CashDeskStandardNewCustomerState(self.context))
