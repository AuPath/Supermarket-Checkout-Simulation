from mesa import Model

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.zones.dinamic.CashDeskZone import CashDeskZone


class CashDeskSelfServiceZone(CashDeskZone):

    def __init__(self, model: Model, cash_desks_number: int):
        super(CashDeskSelfServiceZone, self).__init__(model, cash_desks_number)

    def build(self):
        if self.cash_desks_number == 0:
            pass
        else:
            x = (self.model.cash_desk_self_scan_zone.cash_desks_number * 2 if self.model.cash_desk_self_scan_zone is not None else 0) \
                + 3 + (self.model.cash_desk_standard_zone.cash_desks_number * 2 if self.model.cash_desk_standard_zone is not None else 0) \
                + (self.model.cash_desk_standard_shared_zone.cash_desks_number * 2 if self.model.cash_desk_standard_shared_zone is not None else 0) \
                + 1
            y = 0
            for i, cash_desk in enumerate(self.cash_desks):
                if i % 6 == 0:
                    self.model.grid.place_agent(cash_desk, (x, y))
                elif i % 6 == 1:
                    self.model.grid.place_agent(cash_desk, (x, y + 2))
                elif i % 6 == 2:
                    self.model.grid.place_agent(cash_desk, (x + 2, y))
                elif i % 6 == 3:
                    self.model.grid.place_agent(cash_desk, (x + 2, y + 2))
                elif i % 6 == 4:
                    self.model.grid.place_agent(cash_desk, (x + 4, y))
                elif i % 6 == 5:
                    self.model.grid.place_agent(cash_desk, (x + 4, y + 2))

    def move_to_queue(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            if self.model.grid.is_cell_empty((x + 6, y)):
                x += 2
            elif self.model.grid.is_cell_empty((x + 2, y)):
                x -= 2
            self.model.grid.move_agent(customer, (x, 4 + customer.target_queue.size()))

    def move_customer_beside_cashdesk(self, customer: Customer, cash_desk: CashDesk):
        if customer.target_queue in self.queues:
            (x, y) = cash_desk.pos
            y += 1
            self.model.grid.move_agent(customer, (x, y))
