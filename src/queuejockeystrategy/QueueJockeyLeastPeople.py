from operator import methodcaller
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastPeople(QueueJockeyStrategy):

    def switch_queue(self, customer, other_cash_desks):

        current_cash_desk = customer.get_cash_desk(customer.target_queue)
        customer_pos = current_cash_desk.queue.content().index(customer)
        customer_pos = customer_pos if current_cash_desk.customer is None else customer_pos + 1

        min_other_cash_desk = min(other_cash_desks, key=methodcaller('queue_size'))

        if customer_pos <= min_other_cash_desk.queue_size():
            return current_cash_desk.queue
        else:
            return min_other_cash_desk.queue
