from abc import abstractmethod

from mesa import Model

from src.zones.Zone import Zone


class CashDeskZone(Zone):

    @abstractmethod
    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskZone, self).__init__(model)
        self.cash_desks_number = cash_desks_number
