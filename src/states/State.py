from abc import ABC, abstractmethod
from src.Customer import Customer


class State(ABC):

    def __init__(self, c):
        self.context = c

    @abstractmethod
    def action(self):
        pass
