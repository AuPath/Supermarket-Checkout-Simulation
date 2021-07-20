from operator import methodcaller
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastPeople(QueueJockeyStrategy):

    def switch_queue(self, cash_desks):
        return min(cash_desks, key=methodcaller('queue_size'))
