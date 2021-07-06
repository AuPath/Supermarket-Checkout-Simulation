from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue


class CashDeskStandard(CashDesk):
    def __init__(self, supermarket_queue: SupermarketQueue):
        super().__init__(supermarket_queue)
