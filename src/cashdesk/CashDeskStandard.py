from mesa import Agent

from src.cashdesk.CashDesk import CashDesk
from src.queue.SupermarketQueue import SupermarketQueue

from src.cashdesk.CashDesk import CashDeskState

class CashDeskStandard(Agent, CashDesk):
    def __init__(self, supermarket_queue: SupermarketQueue):
        super().__init__(supermarket_queue)

    def step(self):
        if self.__state == CashDeskState.GET_NEW_CUSTOMER:
            self.serve_new_customer()
            self.__state = CashDeskState.PROCESSING_CUSTOMER
        elif self.__state == CashDeskState.PROCESSING_CUSTOMER:
            if not self.__customer.transaction_is_completed():
                self.process_customer()
            else:
                self.__state = CashDeskState.TRANSACTION_COMPLETED
        elif self.__state == CashDeskState.TRANSACTION_COMPLETED:
            self.complete_transaction()
            self.__state = CashDeskState.GET_NEW_CUSTOMER
