import logging

from src.queuechoicestrategy.QueueChoiceStrategy import QueueChoiceStrategy
from src.cashdesk import CashDesk
from src.cashdesk.CashDeskStandard import CashDeskStandard
from src.cashdesk.CashDeskSelfService import CashDeskSelfService


# Waiting time per ogni coda calcolato come prodotto tra persone in coda (queue.size())
# e tempo service time medio per la tipologia di cassa alla quale la coda fa riferimento


class QueueChoiceLeastWaitingTimeServiceImplied(QueueChoiceStrategy):

    # Assumo che le cash desk escludano quella self scan
    def choose_queue(self, cash_desks):
        # Separo per tipo di cassa, devo farlo per calcolare i tempi medi per tipo di cassa
        normal_cash_desks = list(filter(lambda x: isinstance(x, CashDeskStandard)
                                        , cash_desks))
        self_service_cash_desks = list(filter(lambda x: isinstance(x, CashDeskSelfService)
                                              , cash_desks))

        logging.info("normal cash desks: " + str(len(normal_cash_desks)))
        logging.info("self cash desks: " + str(len(self_service_cash_desks)))

        # Calcolo tempo medio
        # Minimo per tipo di cassa



        if len(normal_cash_desks) > 0 and len(self_service_cash_desks) > 0:
            normal_queues_mean_service_time = self.estimate_mean_service_time(normal_cash_desks)

            normal_queue_min = min(self.get_queues_for_cash_desk_type(normal_cash_desks),
                                   key=lambda x: x.size() * normal_queues_mean_service_time)

            self_service_queues_mean_service_time = self.estimate_mean_service_time(self_service_cash_desks)

            self_service_queue_min = min(self.get_queues_for_cash_desk_type(self_service_cash_desks),
                                         key=lambda x: x.size() * self_service_queues_mean_service_time)

            return normal_queue_min if (normal_queue_min.size() * normal_queues_mean_service_time <=
                                        self_service_queue_min.size() * self_service_queues_mean_service_time) \
                else self_service_queue_min

        elif len(normal_cash_desks) > 0 and len(self_service_cash_desks) == 0:
            normal_queues_mean_service_time = self.estimate_mean_service_time(normal_cash_desks)

            normal_queue_min = min(self.get_queues_for_cash_desk_type(normal_cash_desks),
                                   key=lambda x: x.size() * normal_queues_mean_service_time)

            return normal_queue_min

        else:
            self_service_queues_mean_service_time = self.estimate_mean_service_time(self_service_cash_desks)

            self_service_queue_min = min(self.get_queues_for_cash_desk_type(self_service_cash_desks),
                                         key=lambda x: x.size() * self_service_queues_mean_service_time)

            return self_service_queue_min

    # Da una lista di casse (si assume di tipo omogeneo) ritorna una lista di code associate a quel tipo di cassa
    def get_queues_for_cash_desk_type(self, cash_desks):
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

    # Ritorna il tempo medio di service time per una lista di casse, considera quindi le code associate alle casse
    def estimate_mean_service_time(self, cash_desks: CashDesk):
        mean_service_time = 0
        for c in cash_desks:
            mean_service_time += c.service_time_total()

        return mean_service_time / len(cash_desks)
