from mesa import Model

from src.zones.stationary.StationaryZone import StationaryZone


class EnteringZone(StationaryZone):

    def __init__(self, model: Model, dimension: int):
        super(EnteringZone, self).__init__(model, dimension)

    def build(self):
        x = self.model.grid.width - self.dimension
        for y in range(0, self.model.grid.height - self.model.shopping_zone.dimension):
            cell = self.model.add_occupied_cell(False, "v")
            self.model.grid.place_agent(cell, (x, y))
