from operator import methodcaller

from numpy import random

from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastPeople(QueueJockeyStrategy):

    def __init__(self, threshold, prob_jockey):
        super().__init__()
        self.prob_jockey = prob_jockey  # Probabilità di fare jockey secondo bernoulli
        self.threshold = threshold

    def switch_queue(self, customer, other_cash_desks):

        current_cash_desk = customer.get_cash_desk(customer.target_queue)

        if random.random() <= self.prob_jockey:
            customer_pos = current_cash_desk.queue.content().index(customer)
            customer_pos = customer_pos if current_cash_desk.customer is None else customer_pos + 1

            min_other_cash_desk = min(other_cash_desks, key=methodcaller('queue_size'))

            queue_diff = customer_pos - min_other_cash_desk.queue_size()

            if queue_diff > self.threshold:
                return min_other_cash_desk.queue
            else:
                return current_cash_desk.queue
        else:
            return current_cash_desk.queue
