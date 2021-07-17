from operator import methodcaller
from src.queuejockeystrategy import QueueJockeyStrategy


class QueueJockeyLeastItems(QueueJockeyStrategy):

    def switch_queue(self, queues):
        return min(queues, key=methodcaller('total_items'))
