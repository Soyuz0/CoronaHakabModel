from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.entities import Entity, Circle
from src.states import HealthMachine


class Agent(Entity, ABC):
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


class Location(Circle):
    """
    An infectious circle is a circle of agents in which agents might infect one another
    """
    def __init__(self, area):
        super().__init__()
        
        ## Circle Constant Values ##
        self.area = area # a measure of how big this circle is. Used to calculate density.

        ## Circle Updating Values ##
        self.infectious_count = 0

    def health_changed(self, agent, new_state):
        p_inf = agent.health.infectious
        n_inf = new_state.infectious
        if p_inf != n_inf:
            if n_inf:
                self.infectious_count += 1
            else:
                self.infectious_count -= 1

    def add(self, ent: Agent):
        super().add(ent)
        if ent.health.infectious:
            self.infectious_count += 1

    def remove(self, ent: Agent):
        super().remove(ent)
        if ent.health.infectious:
            self.infectious_count -= 1

    def infected_ratio(self):
        """
        :return: the ratio of infected agents
        """
        return self.infectious_count / len(self.entities)

    def time_passed(self, manager):
        pass  # todo infection logic
        
    def get_density(self):
        if self.area == 0:
            raise Exception("Circe is with area of 0")
        return self.infectious_count / self.area
