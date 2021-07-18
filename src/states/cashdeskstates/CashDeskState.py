from abc import ABC, abstractmethod
from src.states.State import State


class CashDeskState(State, ABC):

    def __init__(self, c):
        self.context = c

    @abstractmethod
    def action(self):
        pass
