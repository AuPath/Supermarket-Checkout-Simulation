from abc import ABC, abstractmethod


class QueueJockeyStrategy(ABC):

    # Must return a single queue
    # Assumo che le code escludano quella self scan
    # Se non conviene cambiare code ritorna la stessa in cui il cliente si trova.
    # Quando ci sará il codice per cambiare coda bisogna cambiare solo se la coda é diversa.

    @abstractmethod
    def switch_queue(self, queues):
        pass
