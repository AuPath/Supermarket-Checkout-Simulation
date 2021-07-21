from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.cashdesk import CashDesk
import math

# Waiting time per ogni coda calcolato come prodotto tra persone in coda (queue.size())
# e tempo service time per la tipologia di cassa alla quale la coda fa riferimento


class QueueChoiceLeastWaitingPowerImplied(QueueChoiceStrategy):

    # Assumo che le cash desk escludano quella self scan
    def choose_queue(self, cash_desks: list[CashDesk]):

        minimum = math.inf
        chosen_queue = None

        for c in cash_desks:
            waiting_time = c.queue_size() * c.service_time_total()
            if minimum > waiting_time:
                minimum = waiting_time
                chosen_queue = c.queue

        return chosen_queue
