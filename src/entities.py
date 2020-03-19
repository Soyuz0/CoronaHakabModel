from __future__ import annotations

from typing import Optional, MutableSet


class Entity:
    __slots__ = 'circles',

    def __init__(self):
        self.circles: Optional[MutableSet[Circle]] = None

    def time_passed(self, manager):
        """
        is called whenever a time period has elapsed
        """
        pass


class Circle(Entity):
    __slots__ = 'entities'

    def __init__(self):
        super().__init__()
        self.entities: MutableSet[Entity] = set()

    def add(self, ent: Entity):
        if ent.circles is None:
            ent.circles = {self}
        else:
            ent.circles.add(self)
        self.entities.add(ent)

    def remove(self, ent: Entity):
        self.entities.remove(ent)
