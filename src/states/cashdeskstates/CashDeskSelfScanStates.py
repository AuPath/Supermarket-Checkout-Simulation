import logging
from random import random

from src.states.State import State
from src.states.customerstates.CustomerAtCashDeskState import CustomerAtCashDeskState
from numpy import cumsum


class CashDeskSelfScanNewCustomerState(State):
    RE_READ_TOTAL_PROBABILITY = 0.01
    RE_READ_PARTIAL_PROBABILITY = 0.03
    NO_READ_PROBABILITY = 1 - (RE_READ_TOTAL_PROBABILITY + RE_READ_PARTIAL_PROBABILITY)

    def __init__(self, c):
        super().__init__(c)
        self.prob_distribution = self.init_prob_distribution()

    def init_prob_distribution(self):
        prob_dist = ((self.no_reading, CashDeskSelfScanNewCustomerState.NO_READ_PROBABILITY),
                     (self.partial_reading, CashDeskSelfScanNewCustomerState.RE_READ_PARTIAL_PROBABILITY),
                     (self.total_reading, CashDeskSelfScanNewCustomerState.RE_READ_TOTAL_PROBABILITY))
        prob_dist_sorted = sorted(prob_dist, key=lambda x: x[1], reverse=True)
        cum_sum_prob = cumsum([x[1] for x in prob_dist_sorted])
        distribution_sorted = list(zip([x[0] for x in prob_dist_sorted], cum_sum_prob))
        return distribution_sorted

    def action(self):

        if self.context.queue.size() > 0:
            self.context.customer = self.context.queue.dequeue()
            rand_num = random()

            for target_action, probability in self.prob_distribution:
                if rand_num <= probability:
                    target_action()
                    break

    def no_reading(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " has acquired customer " + str(self.context.customer.unique_id))

        self.context.customer.state_change(CustomerAtCashDeskState(self.context.customer))
        self.context.move_customer_beside_cashdesk()
        self.context.state_change(CashDeskSelfScanProcessingState(self.context))

        if self.context.queue.size() > 0:
            self.advance_all_customers()

    def partial_reading(self):
        # partial rereading
        self.context.total_reread = False
        self.context.customer.basket_size = 10
        self.context.move_customer_to_reserved_queue()
        self.advance_all_customers()

    def total_reading(self):
        # total rereading
        self.context.total_reread = True
        self.context.move_customer_to_reserved_queue()
        self.advance_all_customers()

    def advance_all_customers(self):
        for customer in self.context.queue.content():
            self.context.advance(customer)


class CashDeskSelfScanProcessingState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " processing customer " + str(self.context.customer.unique_id))

        self.context.process_customer()

        if self.context.is_transaction_complete():
            self.context.customer.exit_store()
            self.context.customer.send_waiting_time()

            logging.info("Customer exited")
            self.context.state_change(CashDeskSelfScanTransactionCompletedState(self.context))


class CashDeskSelfScanTransactionCompletedState(State):

    def action(self):
        logging.info("Cash desk " + type(self.context).__name__ + " " + str(self.context.unique_id) +
                     " completing the transaction")

        # terminato un cliente riprendo ad accettarne di nuovi
        self.context.state_change(CashDeskSelfScanNewCustomerState(self.context))
