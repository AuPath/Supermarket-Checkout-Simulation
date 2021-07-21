import logging
import random

from src.states.State import State
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState


class CashDeskNewCustomerState(State):

    def action(self):
        if self.context.queue.size() > 0:

            # Prendo il cliente e gli cambio lo stato
            self.context.customer = self.context.queue.dequeue()

            logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                         " has acquired customer " + str(self.context.customer.unique_id))

            self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

            self.context.move_beside()

            self.context.state_change(CashDeskProcessingState(self.context))

            if self.context.queue.size() > 0:
                for customer in self.context.queue.content():
                    self.context.advance(customer)


class CashDeskNewCustomerStateSelfScan(CashDeskNewCustomerState):

    def action(self):
        if self.context.queue.size() > 0:
            rand_num = random.random()  # 0.8 niente, 0.15 parziale, 0.05 totale
            if rand_num <= 0.8:
                super().action()
            else:
                # Prendo il cliente e gli cambio lo stato
                self.context.customer = self.context.queue.dequeue()
                if rand_num <= 0.95:
                    # partial rereading
                    self.context.total_reread = False
                    self.context.customer.basket_size = 10
                    self.context.move_customer_to_reserved_queue()
                else:
                    # total rereading
                    self.context.total_reread = True
                    self.context.move_customer_to_reserved_queue()

                for customer in self.context.queue.content():
                    self.context.advance(customer)


class CashDeskNewCustomerStateReserved(CashDeskNewCustomerState):

    def action(self):
        if self.context.queue.size() > 0:

            # precedenza ai parziali
            if len(self.context.partial) > 0:
                # Prendo il cliente e gli cambio lo stato
                self.context.customer = self.context.partial.pop()

                logging.info("Cash desk reserved " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                             " has acquired customer " + str(self.context.customer.unique_id) + " for partial reread")

                self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

                self.context.move_beside()

                self.context.state_change(CashDeskProcessingStateReserved(self.context))

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

                self.context.move_beside()

                self.context.state_change(CashDeskProcessingStateReserved(self.context))

                if self.context.queue.size() > 0:
                    for customer in self.context.queue.content():
                        self.context.advance(customer)


class CashDeskProcessingState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " processing customer " + str(self.context.customer.unique_id))

        self.context.process_customer()

        if self.context.is_transaction_complete():
            self.context.customer.exit_store()

            logging.info("Customer exited")
            self.context.state_change(CashDeskTransactionCompletedStateSelfScan(self.context))


class CashDeskProcessingStateReserved(CashDeskProcessingState):

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
            self.context.customer = None
            logging.info("Customer uscito")
            self.context.state_change(CashDeskTransactionCompletedStateReserved(self.context))


class CashDeskTransactionCompletedState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskNewCustomerState(self.context))


class CashDeskTransactionCompletedStateSelfScan(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskNewCustomerStateSelfScan(self.context))


class CashDeskTransactionCompletedStateReserved(State):

    def action(self):
        logging.info("Cash desk reserved " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskNewCustomerStateReserved(self.context))
