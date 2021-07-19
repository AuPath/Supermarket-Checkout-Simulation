from operator import methodcaller
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastPeople(QueueJockeyStrategy):

    def switch_queue(self, queues):
        return min(queues, key=methodcaller('size'))
