from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue
from src.Customer import Customer
import math


class CashDeskSelfService(CashDesk):

    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)

    def transaction_time(self, c: Customer):
        a = 0.6725
        b = 3.1223
        return math.exp(a * math.log(c.basket_size) + b)

    def break_time(self, c: Customer):
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
