from mesa import Model

from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskSelfScanZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskSelfScanZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            # Delimiting the space
            x = 0
            y = self.model.grid.height - self.model.shopping_zone.dimension - 2
            vertical = True
            for cash_desk in self.cash_desks:
                if vertical:
                    self.model.grid.place_agent(cash_desk, (x, y))
                    y -= 2
                    if y <= 0:
                        vertical = False
                        y = 0
                        x = 2
                else:
                    self.model.grid.place_agent(cash_desk, (x, y))
                    x += 2

            for y in range(0, self.model.grid.height - self.model.shopping_zone.dimension):
                cell = self.model.add_occupied_cell("v")
                self.model.grid.place_agent(cell, (x, y))
