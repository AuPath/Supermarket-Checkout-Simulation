from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self, c):
        self.context = c

    @abstractmethod
    def action(self):
        pass
