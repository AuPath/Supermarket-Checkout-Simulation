import logging

from mesa import Model

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskReservedZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskReservedZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            x = (self.model.cash_desk_self_scan_zone.cash_desks_number * 2
                 if self.model.cash_desk_self_scan_zone is not None else 0) - 1
            y = self.model.grid.height - self.model.shopping_zone.dimension - 2
            cash_desk = self.cash_desks[0]
            self.model.grid.place_agent(cash_desk, (x, y))

    def move_to_reserved_queue(self, customer: Customer, cash_desk: CashDesk):
        cash_desk.queue.enqueue(customer)
        customer.target_queue = cash_desk.queue
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            y = y - customer.target_queue.size() - 1
            self.model.grid.move_agent(customer, (x, y))
            if self.cash_desks[0].total_reread:
                cash_desk.total.append(customer)
            else:
                cash_desk.partial.append(customer)

    def move_beside(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            x -= 1
            self.model.grid.move_agent(customer, (x, y))

    def advance(self, customer: Customer):
        logging.info("Customer " + str(customer.unique_id) + " advancing")
        (x, y) = customer.pos
        self.model.grid.move_agent(customer, (x, y + 1))
