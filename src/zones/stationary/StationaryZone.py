from abc import ABC, abstractmethod

from mesa import Agent

from src.zones.Zone import Zone


class StationaryZone(ABC, Zone):

    @abstractmethod
    def __init__(self, dimension):
        self.dimension = dimension

    def move_to_first_available(self, agent: Agent, destination: (int, int)):
        # TODO
        pass

