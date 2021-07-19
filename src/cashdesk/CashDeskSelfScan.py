from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue


class CashDeskSelfScan(CashDesk):
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)

    def move_beside(self):
        self.model.cash_desk_self_scan_zone.move_beside(self.customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_self_scan_zone.advance(customer)
