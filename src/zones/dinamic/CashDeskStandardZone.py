import math

from mesa import Model

from src.Customer import Customer
from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskStandardZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskStandardZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            x = ((self.model.cash_desk_self_scan_zone.cash_desks_number - math.ceil((
                                                                                            self.model.grid.height - self.model.shopping_zone.dimension - 2) / 2)) * 2 if self.model.cash_desk_self_scan_zone is not None else 0)
            x = (x if x >= 0 else 0) + 4
            y = 0
            for cash_desk in self.cash_desks:
                self.model.grid.place_agent(cash_desk, (x, y))
                x += 2

    def move_to_queue(self, customer: Customer):
        if customer.target_queue in self.queues:
            (x, y) = self.get_cash_desk(customer.target_queue).pos
            y = 2 + customer.target_queue.size()
            self.model.grid.move_agent(customer, (x, y))
