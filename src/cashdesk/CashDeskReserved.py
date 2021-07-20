from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.cashdeskstates.CashDeskStates import CashDeskNewCustomerStateReserved


class CashDeskReserved(CashDesk):
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)
        self.state_change(CashDeskNewCustomerStateReserved(self))
        self.total_reread = False
        self.partial = []
        self.total = []

    def move_beside(self):
        self.model.cash_desk_reserved_zone.move_beside(self.customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_reserved_zone.advance(customer)

    def process_customer_partial(self):
        c = self.customer
        c.basket_size = 0

    def process_customer_total(self):
        c = self.customer

        if c.basket_size - self.__processing_speed <= 0:
            c.basket_size = 0
        else:
            c.basket_size -= self.__processing_speed
