from functools import reduce
from operator import methodcaller
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastItems(QueueJockeyStrategy):

    def switch_queue(self, customer, other_cash_desks):
        # todo considerare quello in cassa, devo considerare diversamente la coda dove mi trovo rispetto alle altre
        if not other_cash_desks:
            return None

        current_cash_desk = customer.get_cash_desk(customer.target_queue)

        customers_in_queue = customer.target_queue.content()
        customer_pos = customers_in_queue.index(customer)
        customers_before_customer = customers_in_queue[:customer_pos]

        if current_cash_desk.customer is not None:
            customers_before_customer.append(current_cash_desk.customer)

        current_queue_total_items = 0
        for c in customers_before_customer:
            current_queue_total_items += c.basket_size

        min_other_cash_desks = min(other_cash_desks, key=methodcaller('total_items'))

        return current_cash_desk.queue if current_queue_total_items <= min_other_cash_desks.total_items() \
            else min_other_cash_desks.queue
