from mesa import Model

from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskSelfServiceZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskSelfServiceZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
