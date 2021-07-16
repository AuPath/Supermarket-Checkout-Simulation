from operator import methodcaller

from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy


class QueueChoiceLeastPeople(QueueChoiceStrategy):

    # Returns shortest/smalles queue from queues, the comparison is made on the
    # basis of the size() function of the queues
    def choose_queue(self, queues: list, self_scan: bool):
        return min(queues, key=methodcaller('size'))
