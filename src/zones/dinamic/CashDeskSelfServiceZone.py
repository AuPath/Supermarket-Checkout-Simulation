import math

from mesa import Model

from src.OccupiedCell import CashDeskType
from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskSelfServiceZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskSelfServiceZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            number_self_scan = (self.model.cash_desk_self_scan_zone.cash_desks_number - math.ceil((self.model.grid.height - self.model.shopping_zone.dimension - 2) / 2)) * 2
            x = ((number_self_scan if number_self_scan >= 0 else 0) + 4 if self.model.cash_desk_self_scan_zone is not None else 0)
            x += (self.model.cash_desk_standard_zone.cash_desks_number if self.model.cash_desk_standard_zone is not None else 0)*2 + 1
            y = 0
            for cash_desk in range(self.cash_desks_number):
                cell = self.model.add_occupied_cell("", CashDeskType.SELF_SERVICE)
                self.model.grid.place_agent(cell, (x, y))
                cell = self.model.add_occupied_cell("", CashDeskType.SELF_SERVICE)
                self.model.grid.place_agent(cell, (x, y + 2))
                cell = self.model.add_occupied_cell("", CashDeskType.SELF_SERVICE)
                self.model.grid.place_agent(cell, (x + 2, y))
                cell = self.model.add_occupied_cell("", CashDeskType.SELF_SERVICE)
                self.model.grid.place_agent(cell, (x + 2, y + 2))
                x += 5

