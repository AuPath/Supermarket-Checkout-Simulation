from mesa import Model

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskStandardZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskStandardZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            x = (self.model.cash_desk_self_scan_zone.cash_desks_number * 2
                 if self.model.cash_desk_self_scan_zone is not None else 0) + 3
            y = 0
            for cash_desk in self.cash_desks:
                self.model.grid.place_agent(cash_desk, (x, y))
                x += 2

    def move_to_queue(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            y = 1 + customer.target_queue.size()
            self.model.grid.move_agent(customer, (x, y))

    def move_beside(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            x -= 1
            self.model.grid.move_agent(customer, (x, y))
