from operator import methodcaller
from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.cashdesk import CashDesk


class QueueChoiceLeastPeople(QueueChoiceStrategy):

    # Returns shortest/smallest queue from queues, the comparison is made on the
    # basis of the size() function of the queues
    def choose_queue(self, cash_desks: list[CashDesk]):

        queues = []
        for c in cash_desks:
            queues.append(c.queue)

        return min(queues, key=methodcaller('size'))
