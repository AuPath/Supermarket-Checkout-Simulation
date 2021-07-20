from operator import methodcaller
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastItems(QueueJockeyStrategy):

    def switch_queue(self, cash_desks):
        queues = []
        for c in cash_desks:
            queues.append(c.queue)

        return min(queues, key=methodcaller('total_items'))
