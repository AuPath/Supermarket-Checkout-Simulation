import logging

from src.states.State import State
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState


class CashDeskReservedNewCustomerState(State):

    def action(self):
        if self.context.queue.size() > 0:

            # precedenza ai parziali
            if len(self.context.partial) > 0:
                # Prendo il cliente e gli cambio lo stato
                self.context.customer = self.context.partial.pop()

                logging.info("Cash desk reserved " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                             " has acquired customer " + str(self.context.customer.unique_id) + " for partial reread")

                self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

                self.context.move_customer_beside_cashdesk()

                self.context.state_change(CashDeskReservedProcessingState(self.context))

                queue_before_customer = self.context.queue.content()
                i = queue_before_customer.index(self.context.customer)
                queue_before_customer = queue_before_customer[i + 1:]
                self.context.queue.remove_element(self.context.customer)
                if len(queue_before_customer):
                    for customer in queue_before_customer:
                        self.context.get_cash_desk(self.context.target_queue).advance(customer)
            else:
                # Prendo il cliente e gli cambio lo stato
                self.context.customer = self.context.queue.dequeue()

                logging.info("Cash desk reserved " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                             " has acquired customer " + str(self.context.customer.unique_id) + " for total reread")

                self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

                self.context.move_customer_beside_cashdesk()

                self.context.state_change(CashDeskReservedProcessingState(self.context))

                if self.context.queue.size() > 0:
                    for customer in self.context.queue.content():
                        self.context.advance(customer)


class CashDeskReservedProcessingState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " processing customer " + str(self.context.customer.unique_id))

        if self.context.total_reread:
            # total rereading
            self.context.process_customer_total()
        else:
            # partial rereading
            self.context.process_customer_partial()

        if self.context.is_transaction_complete():
            self.context.customer.exit_store()
            self.context.customer.send_waiting_time()
            self.context.customer = None
            logging.info("Customer uscito")
            self.context.state_change(CashDeskReservedTransactionCompletedState(self.context))


class CashDeskReservedTransactionCompletedState(State):

    def action(self):
        logging.info("Cash desk reserved " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskReservedNewCustomerState(self.context))