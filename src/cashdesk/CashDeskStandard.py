from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue


class CashDeskStandard(CashDesk):

    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)
        self.a_transaction = 0.6984
        self.b_transaction = 2.1219
        self.a_break = 0.2251
        self.b_break = 3.5167

    def move_beside(self, customer: Customer):
        self.model.cash_desk_standard_zone.move_beside(customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_standard_zone.advance(customer)
