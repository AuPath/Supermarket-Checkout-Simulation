from src.Customer import Customer
from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue
from src.states.cashdeskstates.CashDeskSelfServiceStates import CashDeskSelfServiceNewCustomerState

# TODO: A cosa serve questo parametro questo parametro?
PROCESSING_SPEED_SLOWER = 1.5


class CashDeskSelfService(CashDesk):
    def __init__(self, agent_id, model, supermarket_queue: SupermarketQueue):
        super().__init__(agent_id, model, supermarket_queue)
        self.state_change(CashDeskSelfServiceNewCustomerState(self))
        self.processing_speed = self.processing_speed / PROCESSING_SPEED_SLOWER
        self.a_transaction = 0.6725
        self.b_transaction = 3.1223
        self.a_break = 0.2251
        self.b_break = 3.5167

    def move_customer_beside_cashdesk(self):
        self.model.cash_desk_self_service_zone.move_customer_beside_cashdesk(self.customer, self)

    def advance(self, customer: Customer):
        self.model.cash_desk_self_service_zone.advance(customer)

    def get_image(self):
        return "images/aSquare.png"
