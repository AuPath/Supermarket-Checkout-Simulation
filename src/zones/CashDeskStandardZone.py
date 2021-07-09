from mesa import Agent

from src.zones.CashDeskZone import CashDeskZone


class CashDeskStandardZone(CashDeskZone):

    def __init__(self, dimension):
        self.dimension = dimension

    def build(self):
        pass


