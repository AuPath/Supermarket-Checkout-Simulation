from abc import abstractmethod

from mesa import Model

from src.zones.Zone import Zone


class CashDeskZone(Zone):

    @abstractmethod
    def __init__(self, model: Model, dimension: int):
        super(CashDeskZone, self).__init__(model)
        self.dimension = dimension


