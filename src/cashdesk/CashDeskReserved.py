from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.cashdeskstates.CashDeskReservedStates import CashDeskReservedNewCustomerState


class CashDeskReserved(CashDesk):
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)
        self.state_change(CashDeskReservedNewCustomerState(self))
        self.total_reread = False
        self.partial = []
        self.total = []

    def move_customer_beside_cashdesk(self):
        self.model.cash_desk_reserved_zone.move_customer_beside_cashdesk(self.customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_reserved_zone.advance(customer)

    def process_customer_partial(self):
        c = self.customer

        if c.basket_size - self.processing_speed <= 0:
            c.basket_size = 0
        else:
            c.basket_size -= self.processing_speed

    def process_customer_total(self):
        c = self.customer

        if c.basket_size - self.processing_speed <= 0:
            c.basket_size = 0
        else:
            c.basket_size -= self.processing_speed

    def get_image(self):
        return "images/nSquare.png"
