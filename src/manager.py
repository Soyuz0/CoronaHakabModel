from __future__ import annotations

from itertools import chain
from typing import Iterable, Callable

from src.agent import Agent, Location


class SimulationManager:
    def __init__(self, agents: Iterable[Agent], locations: Iterable[Location]):
        self.locations = list(locations)
        self.agents = list(agents)

        self.logger: Callable[[SimulationManager],None] = lambda x:None  # todo
        self.to_continue: Callable[[SimulationManager], bool] = lambda x: False  # todo

    def step(self):
        # move stage
        dests = [(a, a.next_location(self)) for a in self.agents]
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
        while self.to_continue(self):
            self.step()

    # todo add and remove agents/locations
