import logging
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

    def move_to_queue(self, customer: Customer, cash_desk: CashDesk):
        pass

    def move_beside(self, customer: Customer, cash_desk: CashDesk):
        pass

    def advance(self, customer: Customer):
        logging.info("Customer " + str(customer.unique_id) + " advancing")
        (x, y) = customer.pos
        self.model.grid.move_agent(customer, (x, y - 1))

    @property
    def queues(self):
        return [cash_desk.queue for cash_desk in self.cash_desks]
