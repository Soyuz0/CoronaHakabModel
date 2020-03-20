from random import choice
from typing import Optional

from src.agent import Location, Agent


class SmurfHome(Location):
    pass


class Smurf(Agent):
    def __init__(self, home: SmurfHome):
        super().__init__(home, id(self))
        self.home = home

    def next_location(self, manager) -> Optional[Location]:
        """
        smurf script:
        0- do nothing
        1- go to random home
        2- go home
        3- do nothing
        """
        t = manager.sim_time % 4
        if t in (0, 3):
            return None
        if t == 1:
            # todo improve
            while (rand_home := choice(manager.locations)) != self.home:
                pass
            return rand_home
        return self.home
