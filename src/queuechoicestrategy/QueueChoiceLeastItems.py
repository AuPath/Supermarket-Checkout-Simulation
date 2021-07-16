import math
from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.cashdesk import CashDesk


class QueueChoiceLeastItems(QueueChoiceStrategy):

    # Returns shortest/smallest queue from queues, the comparison is made on the
    # basis of the size() function of the queues
    def choose_queue(self, cash_desks: list[CashDesk]):

        queues = []
        for c in cash_desks:
            queues.append(c.queue)

        minimum = math.inf
        chosen_queue = None

        # Find queue with least items
        for q in queues:
            if q.total_items() < minimum:
                minimum = q.total_items()
                chosen_queue = q
            
        return chosen_queue

