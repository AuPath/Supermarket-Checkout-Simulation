import math

from mesa import Model

from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskStandardZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskStandardZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            x = ((self.model.cash_desk_self_scan_zone.cash_desks_number - math.ceil((self.model.grid.height - self.model.shopping_zone.dimension - 2) / 2))*2 + 4 if self.model.cash_desk_self_scan_zone is not None else 0)
            y = 0
            for cash_desk in range(self.cash_desks_number):
                cell = self.model.add_occupied_cell(True)
                self.model.grid.place_agent(cell, (x, y))
                x += 2
