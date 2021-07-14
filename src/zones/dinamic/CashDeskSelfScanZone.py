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
            cash_desks = self.cash_desks_number
            while y > 0 and cash_desks > 0:
                cell = self.model.add_occupied_cell(True)
                self.model.grid.place_agent(cell, (x, y))
                y -= 2
                cash_desks -= 1

            x = 2
            y = 0
            while cash_desks > 0:
                cell = self.model.add_occupied_cell(True)
                self.model.grid.place_agent(cell, (x, y))
                x += 2
                cash_desks -= 1

            for y in range(0, self.model.grid.height - self.model.shopping_zone.dimension):
                cell = self.model.add_occupied_cell(False, "v")
                self.model.grid.place_agent(cell, (x, y))
