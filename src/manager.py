from __future__ import annotations

from itertools import chain
from typing import Iterable, Callable

from src.agent import Agent, Location
from src.infection import InfectionManager
from src.move import MoveManager


class SimulationManager:
    """
    A simulation manager is the main class, it holds all the locations and agents in the
     simulation and oversees their coordination
    """

    def __init__(self, location_generator, agent_generator, move_policy, infection_policy):
        self.locations = location_generator()
        self.agents = agent_generator(self.locations)

        self.move_manager = MoveManager(self, move_policy)
        self.infection_manager = None  # todo

        self.sim_time: float = None  # sim_time is measured in steps performed, and not in any real-time measurement

        self.logger: Callable[[SimulationManager], None] = lambda x: None  # todo
        self.to_continue: Callable[[SimulationManager], bool] = lambda x: False  # todo

    def step(self):
        self.sim_time += 1
        # move stage
        self.move_manager.step()

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
