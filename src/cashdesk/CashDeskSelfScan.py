from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.cashdeskstates.CashDeskStates import CashDeskNewCustomerStateSelfScan


class CashDeskSelfScan(CashDesk):
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)
        self.state_change(CashDeskNewCustomerStateSelfScan(self))

    def move_customer_beside_cashdesk(self):
        self.model.cash_desk_self_scan_zone.move_customer_beside_cashdesk(self.customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_self_scan_zone.advance(customer)

    def move_customer_to_reserved_queue(self):
        self.model.cash_desk_reserved_zone.move_to_reserved_queue(self.customer,
                                                         self.model.cash_desk_reserved_zone.cash_desks[0])

    def process_customer(self):
        c = self.customer
        c.basket_size = 0

    def get_image(self):
        return "images/sSquare.png"
