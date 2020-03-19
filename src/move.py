from abc import ABC, abstractmethod


class MoveManager:
    """
    Manages the "Move" stage of the simulation.
    """

    def step(self):
        pass


class MovePolicy(ABC):
    """
    Holds relevant information about policys that effect movement generaly.
    """

    @abstractmethod
    def get_next_location(self):
        pass
