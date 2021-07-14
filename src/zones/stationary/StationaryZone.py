from abc import abstractmethod

from mesa import Agent, Model

from src.zones.Zone import Zone


class StationaryZone(Zone):

    @abstractmethod
    def __init__(self, model: Model, dimension: int):
        super(StationaryZone, self).__init__(model)
        self.dimension = dimension

    def move_to_first_available(self, agent: Agent):
        while True:
            position = self.model.random.randrange(self.model.grid.width), self.model.random.randrange(
                self.model.grid.height - self.dimension + 1, self.model.grid.height)
            if self.model.grid.is_cell_empty(position):
                self.model.grid.move_agent(agent, position)
                return

    def is_agent_in_zone(self, agent: Agent):
        (x, y) = agent.pos
        if self.model.grid.height - self.dimension < y <= self.model.grid.height:
            return True
        return False
