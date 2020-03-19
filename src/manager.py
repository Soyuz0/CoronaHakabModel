from __future__ import annotations

from itertools import chain
from typing import Iterable, Callable

from src.agent import Agent, Location


class SimulationManager:
    """
    A simulation manager is the main class, it holds all the locations and agents in the
     simulation and oversees their coordination
    """
    def __init__(self, agents: Iterable[Agent], locations: Iterable[Location]):
        self.locations = list(locations)
        self.agents = list(agents)

        self.sim_time: float = None  # sim_time is measured in steps performed, and not in any real-time measurement

        self.logger: Callable[[SimulationManager],None] = lambda x:None  # todo
        self.to_continue: Callable[[SimulationManager], bool] = lambda x: False  # todo

    def step(self):
        self.sim_time += 1
        # move stage
        dests = [(a, d) for a in self.agents if (d := a.next_location(self))]
        for a,t in dests:
            a.move_to(t)

        # infection stage
        for entity in chain(
            self.agents,
            self.locations
        ):
            entity.time_passed(self)

        self.logger(self)

    def repeat(self):
        self.sim_time = 0
        while self.to_continue(self):
            self.step()

    # todo add and remove agents/locations
