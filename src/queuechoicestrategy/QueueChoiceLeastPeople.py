from operator import methodcaller
from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.cashdesk import CashDesk


class QueueChoiceLeastPeople(QueueChoiceStrategy):

    # Returns shortest/smallest queue from queues, the comparison is made on the
    # basis of the size() function of the queues
    def choose_queue(self, cash_desks):
        chosen_cash_desk = min(cash_desks, key=methodcaller('queue_size'))
        return chosen_cash_desk.queue

