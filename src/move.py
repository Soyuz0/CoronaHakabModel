from __future__ import annotations


class MoveManager:
    """
    Manages the "Move" stage of the simulation.
    """

    def __init__(self, policy: MovePolicy):
        self.owner = None
        self.policy = policy

    def step(self):
        destinations = [(a, d) for a in self.owner.agents if (d := self.policy.get_next_location(a, self.owner))]
        for a, t in destinations:
            a.move_to(t)


class MovePolicy:
    """
    Holds relevant information about policys that effect movement generaly.
    """

    def get_next_location(self, agent, manager):
        return agent.next_location(manager)
