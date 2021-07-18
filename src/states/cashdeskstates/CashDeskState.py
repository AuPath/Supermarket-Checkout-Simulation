from abc import ABC, abstractmethod
from src.states.State import State
from src.cashdesk.CashDesk import CashDesk

class CashDeskState(State, ABC):

    def __init__(self, c: CashDesk):
        self.context = c

    @abstractmethod
    def action(self):
        pass
