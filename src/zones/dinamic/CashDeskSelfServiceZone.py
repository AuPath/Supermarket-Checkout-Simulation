import math

from mesa import Model

from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskSelfServiceZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskSelfServiceZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            number_self_scan = (self.model.cash_desk_self_scan_zone.cash_desks_number - math.ceil(
                (self.model.grid.height - self.model.shopping_zone.dimension - 2) / 2)) * 2
            x = ((
                     number_self_scan if number_self_scan >= 0 else 0) + 4 if self.model.cash_desk_self_scan_zone is not None else 0)
            x += (
                     self.model.cash_desk_standard_zone.cash_desks_number if self.model.cash_desk_standard_zone is not None else 0) * 2 + 1
            y = 0
            for i, cash_desk in enumerate(self.cash_desks):
                if i % 4 == 0:
                    self.model.grid.place_agent(cash_desk, (x, y))
                elif i % 4 == 1:
                    self.model.grid.place_agent(cash_desk, (x, y + 2))
                elif i % 4 == 2:
                    self.model.grid.place_agent(cash_desk, (x + 2, y))
                elif i % 4 == 3:
                    self.model.grid.place_agent(cash_desk, (x + 2, y + 2))
                    x += 5
