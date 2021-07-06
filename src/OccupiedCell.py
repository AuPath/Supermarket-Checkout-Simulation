from mesa import Agent


class OccupiedCell(Agent):
    """This class represents an occupied cell in the canvas of the supermarket."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.type = 1
