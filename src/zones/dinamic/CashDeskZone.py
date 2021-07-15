from abc import abstractmethod

from mesa import Model

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.zones.Zone import Zone


class CashDeskZone(Zone):

    @abstractmethod
    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskZone, self).__init__(model)
        self.cash_desks_number = cash_desks_number
        self.cash_desks = []

    def move_to_queue(self, customer: Customer):
        pass

    def get_cash_desk(self, queue):
        for cash_desk in self.cash_desks:
            if cash_desk.queue == queue:
                return cash_desk

    @property
    def queues(self):
        return [cash_desk.queue for cash_desk in self.cash_desks]
