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
        pass
