from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

class Agent(ABC):
    """
    Aan agent is an entity that can move between locations
    its location is a specific circle that represents a physical location
    """
    __slots__ = "initial_location", "health"

    def __init__(self, initial_location: Location, agent_id):
        super().__init__()

        self.location = initial_location
        initial_location.add(self)

        ## Agent Constant Values ##
        self.agent_id = agent_id

        ## Agent Updating Values ##
        self.health = HealthMachine[0]
        self.infection_rate = 0 # The amount in which the agent is infectious.

    @abstractmethod
    def next_location(self, manager) -> Optional[Location]:
        """
        Get the location the agent will move to within the next time step, or None if no movement will occur
        """
        pass

    def move_to(self, destination: Location):
        """
        Change an agent's location
        """
        self.location.remove(self)
        self.location = destination
        destination.add(self)

    def change_health(self, new_state):
        """
        Change the agent's health state
        """
        for c in self.circles:
            if isinstance(c, Location):  # todo slow?
                c.health_changed(self, new_state)
        self.health = new_state

    def time_passed(self, manager):
        if n_health := self.health.next():
            self.change_health(n_health)
