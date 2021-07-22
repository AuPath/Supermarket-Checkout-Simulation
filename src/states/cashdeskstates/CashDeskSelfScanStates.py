import logging
from random import random

from src.states.State import State
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState


class CashDeskSelfScanNewCustomerState(State):
    RE_READ_PARTIAL_PROBABILITY = 0.075
    RE_READ_TOTAL_PROBABILITY = 0.025
    NO_READ_PROBABILITY = 1 - (RE_READ_TOTAL_PROBABILITY + RE_READ_PARTIAL_PROBABILITY)

    def action(self):
        if self.context.queue.size() > 0:
            rand_num = random()  # 0.8 niente, 0.15 parziale, 0.05 totale
            if rand_num <= 0.9:
                # Prendo il cliente e gli cambio lo stato
                self.context.customer = self.context.queue.dequeue()

                logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                             " has acquired customer " + str(self.context.customer.unique_id))

                self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))

                self.context.move_customer_beside_cashdesk()

                self.context.state_change(CashDeskSelfScanProcessingState(self.context))

                if self.context.queue.size() > 0:
                    for customer in self.context.queue.content():
                        self.context.advance(customer)
            else:
                # Prendo il cliente e gli cambio lo stato
                self.context.customer = self.context.queue.dequeue()
                if rand_num <= 0.975:
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


class CashDeskSelfScanProcessingState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " processing customer " + str(self.context.customer.unique_id))

        self.context.process_customer()

        if self.context.is_transaction_complete():
            self.context.customer.exit_store()

            logging.info("Customer exited")
            self.context.state_change(CashDeskSelfScanTransactionCompletedState(self.context))


class CashDeskSelfScanTransactionCompletedState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskSelfScanNewCustomerState(self.context))