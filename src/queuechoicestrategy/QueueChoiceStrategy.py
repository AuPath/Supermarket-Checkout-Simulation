from abc import ABC, abstractmethod
from src.cashdesk import CashDesk



class QueueChoiceStrategy(ABC):

    # Must return a single queue
    # Assumo che le cash desk escludano quella self scan
    @abstractmethod
    def choose_queue(self, cash_desks: list[CashDesk]):
        pass
