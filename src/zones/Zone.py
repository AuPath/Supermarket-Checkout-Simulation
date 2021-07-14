from abc import ABC, abstractmethod

from mesa import Agent, Model


class Zone(ABC):

    @abstractmethod
    def __init__(self, model: Model):
        self.model = model

    def build(self):
        pass

    def is_agent_in_zone(self, agent: Agent):
        pass
