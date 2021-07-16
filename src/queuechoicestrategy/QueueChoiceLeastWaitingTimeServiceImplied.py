from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.cashdesk import CashDesk, CashDeskStandard, CashDeskSelfService

# Waiting time per ogni coda calcolato come prodotto tra persone in coda (queue.size())
# e tempo service time medio per la tipologia di cassa alla quale la coda fa riferimento


class QueueChoiceLeastWaitingTimeServiceImplied(QueueChoiceStrategy):

    # Assumo che le cash desk escludano quella self scan
    def choose_queue(self, cash_desks: list[CashDesk]):

        # Separo per tipo di cassa, devo farlo per calcolare i tempi medi per tipo di cassa
        normal_cash_desks = list(filter(cash_desks, lambda x: isinstance(x, CashDeskStandard)))
        self_service_cash_desks = list(filter(cash_desks, lambda x: isinstance(x, CashDeskSelfService)))

        # Calcolo tempo medio
        normal_queues_mean_service_time = self.mean_service_time(normal_cash_desks)
        self_service_queues_mean_service_time = self.mean_service_time(self_service_cash_desks)

        # Minimo per tipo di cassa
        normal_queue_min = min(self.get_queues_for_cash_desk_type(normal_cash_desks),
                               key=lambda x: x.size() * normal_queues_mean_service_time)

        self_service_queue_min = min(self.get_queues_for_cash_desk_type(self_service_cash_desks),
                                     key=lambda x: x.size() * self_service_queues_mean_service_time)

        # Minimo assoluto
        return normal_queue_min if (normal_queue_min.size() * normal_queues_mean_service_time <=
                                    self_service_queue_min.size() * self_service_queues_mean_service_time) \
            else self_service_queue_min

    # Da una lista di casse (si assume di tipo omogeneo) ritorna una lista di code associate a quel tipo di cassa
    def get_queues_for_cash_desk_type(self, cash_desks: list[CashDesk]):
        queues = []
        for c in cash_desks:
            queues.append(c.queue)
        return queues

    # Ritorna il tempo medio di service time per una lista di casse, considera quindi le code associate alle casse
    def mean_service_time(self, cash_desks: CashDesk):
        mean_service_time = 0
        for c in cash_desks:
            mean_service_time += c.service_time_total()

        return mean_service_time / len(cash_desks)
