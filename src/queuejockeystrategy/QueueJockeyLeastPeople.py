from operator import methodcaller
from src.queuejockeystrategy.QueueJockeyStrategy import QueueJockeyStrategy


class QueueJockeyLeastPeople(QueueJockeyStrategy):

    def switch_queue(self, cash_desks):
        chosen_cash_desk = min(cash_desks, key=methodcaller('queue_size'))
        return chosen_cash_desk.queue
