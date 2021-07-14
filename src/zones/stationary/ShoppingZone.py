from mesa import Model

from src.zones.stationary.StationaryZone import StationaryZone


class ShoppingZone(StationaryZone):

    def __init__(self, model: Model, dimension: int):
        super(ShoppingZone, self).__init__(model, dimension)

    def build(self):
        y = self.model.grid.height - self.dimension
        for x in range(0, self.model.grid.width - self.model.entering_zone.dimension):
            if x != 1:
                cell = self.model.add_occupied_cell("h")
                self.model.grid.place_agent(cell, (x, y))
