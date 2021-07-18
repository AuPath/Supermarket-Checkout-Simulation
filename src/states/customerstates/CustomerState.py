from abc import ABC, abstractmethod
from src.states.State import State
from src.Customer import Customer


class CustomerState(State, ABC):

    def __init__(self, c: Customer):
        self.context = c

    @abstractmethod
    def action(self):
        pass
