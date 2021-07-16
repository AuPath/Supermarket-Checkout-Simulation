import math

from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue


class CashDeskStandard(CashDesk):

    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)

    def transaction_time(self, c: Customer):
        a = 0.6984
        b = 2.1219
        return math.exp(a * math.log(c.basket_size) + b)

    def break_time(self, c: Customer):  # TODO: non la calcola cosi, la lascio cosí perché almeno si puó testare
        a = 0.2251
        b = 3.5167
        return math.exp(a * math.log(c.basket_size) + b)

    def service_time(self, c: Customer):
        return self.transaction_time(c) + self.break_time(c)

    def service_time_total(self):
        total = 0
        for c in self.queue.content():
            total += self.service_time(c)
        return total
