from __future__ import annotations


class Agent():
    __slots__ = "ID", "health_status", "home", "work"

    def __init__(self, id, health="default"):  # todo add health status
        self.ID = id
        self.home = None
        self.work = None
        self.health_status = health

    def add_home(self, home):
        self.home = home

    def add_work(self, work):
        self.work = work

    def change_health_status(self, new_status):
        self.health_status = new_status

    def __cmp__(self, other):
        return self.ID == other.ID


class Circle:
    __slots__ = "type", "agents"

    def __init__(self, type):
        self.type = type
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_indexes_of_my_circle(self, my_index):
        rest_of_circle = set(map(lambda o: o.ID, self.agents))
        rest_of_circle.remove(my_index)
        return rest_of_circle