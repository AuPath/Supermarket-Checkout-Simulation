from abc import ABC, abstractmethod

class QueueChoiceStrategy(ABC):

    # Must return a single list
    @abstractmethod
    def choose_queue(self, queues: List):
        pass