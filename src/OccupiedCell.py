from enums import Enum
from mesa import Agent


class CashDeskType(Enum):
    NONE = 0
    STANDARD = 1
    SELF_SERVICE = 2
    SELF_SCAN = 3
    RESERVED = 4


class OccupiedCell(Agent):
    """This class represents an occupied cell in the canvas of the supermarket."""

    def __init__(self, unique_id, model, direction="", cash_desk_type=CashDeskType.NONE):
        super().__init__(unique_id, model)

        self.type = 1
        self.cash_desk_type = cash_desk_type
        self.direction = direction
