from abc import ABC, abstractmethod


from src.zones.Zone import Zone


class CashDeskZone(ABC, Zone):

    @abstractmethod
    def __init__(self, dimension):
        self.dimension = dimension


