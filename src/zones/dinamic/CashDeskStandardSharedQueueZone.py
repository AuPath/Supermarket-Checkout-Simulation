from mesa import Model

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.zones.dinamic.CashDeskStandardZone import CashDeskStandardZone


class CashDeskStandardSharedQueueZone(CashDeskStandardZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskStandardSharedQueueZone, self).__init__(model, cash_desks_number)

    def build(self):
        super().build()
        cell = self.model.add_occupied_cell("h")
        x = (self.model.cash_desk_self_scan_zone.cash_desks_number * 2
             if self.model.cash_desk_self_scan_zone is not None else 0) + 3
        y = 3
        self.model.grid.place_agent(cell, (x, y))

    def move_to_queue(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            x = (self.model.cash_desk_self_scan_zone.cash_desks_number * 2
                 if self.model.cash_desk_self_scan_zone is not None else 0) + 3
            y = 4 + customer.target_queue.size()
            self.model.grid.move_agent(customer, (x, y))
