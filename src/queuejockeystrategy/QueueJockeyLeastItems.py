from operator import methodcaller

from numpy import random

from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastItems(QueueJockeyStrategy):

    def __init__(self, threshold, prob_jockey):
        super().__init__()
        self.prob_jockey = prob_jockey  # Probabilità di fare jockey secondo bernoulli
        self.threshold = threshold

    def switch_queue(self, customer, other_cash_desks):

        current_cash_desk = customer.get_cash_desk(customer.target_queue)

        if random.random() <= self.prob_jockey:

            customers_in_queue = customer.target_queue.content()
            customer_pos = customers_in_queue.index(customer)
            customers_before_customer = customers_in_queue[:customer_pos]

            if current_cash_desk.customer is not None:
                customers_before_customer.append(current_cash_desk.customer)

            current_queue_total_items = 0
            for c in customers_before_customer:
                current_queue_total_items += c.basket_size

            min_other_cash_desks = min(other_cash_desks, key=methodcaller('total_items'))

            queue_diff = current_queue_total_items - min_other_cash_desks.total_items()

            if queue_diff > self.threshold:
                return min_other_cash_desks.queue
            else:
                return current_cash_desk.queue
        else:
            return current_cash_desk.queue
