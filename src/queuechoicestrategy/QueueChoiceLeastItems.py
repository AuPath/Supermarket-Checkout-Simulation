from operator import methodcaller
import math

from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy


class QueueChoiceLeastItems(QueueChoiceStrategy):

    # Returns shortest/smalles queue from queues, the comparison is made on the
    # basis of the size() function of the queues
    def choose_queue(self, queues: list, self_scan: bool):
        min = math.inf
        chosen_queue = None

        # Find queue with least items
        for q in queues:
            if q.total_items() < min:
                chosen_queue = q
            
        return chosen_queue

