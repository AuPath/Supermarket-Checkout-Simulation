from mesa import Model

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskSelfScanZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskSelfScanZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            x = 1
            y = 0
            for cash_desk in self.cash_desks:
                self.model.grid.place_agent(cash_desk, (x, y))
                x += 2

            for y in range(0, self.model.grid.height - self.model.shopping_zone.dimension):
                cell = self.model.add_occupied_cell("v")
                self.model.grid.place_agent(cell, (x, y))

    def move_to_queue(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            y = 2 + customer.target_queue.size()
            self.model.grid.move_agent(customer, (x, y))

    def move_beside(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            y += 1
            self.model.grid.move_agent(customer, (x, y))

