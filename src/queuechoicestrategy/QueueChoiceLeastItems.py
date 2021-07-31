from operator import methodcaller
from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy


class QueueChoiceLeastItems(QueueChoiceStrategy):

    # Returns shortest/smallest queue from queues, the comparison is made on the
    # basis of the size() function of the queues

    def choose_queue(self, cash_desks):
        queues = []
        for c in cash_desks:
            queues.append(c.queue)

        return min(queues, key=methodcaller('estimate_total_items'))

