from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue


class CashDeskSelfService(CashDesk):

    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)
        self.a_transaction = 0.6725
        self.b_transaction = 3.1223
        self.a_break = 0.2251
        self.b_break = 3.5167
