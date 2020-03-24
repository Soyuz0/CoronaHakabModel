from __future__ import annotations

from abc import ABC, abstractmethod
from collections import namedtuple
from typing import List, Dict, Set, Optional, Iterable, Collection, Union, Tuple, Sequence

from scipy.stats import rv_discrete, uniform, triang, randint
import numpy as np

from agent import Circle, Agent

PendingTransfer = namedtuple("PendingTransfer", ["agent_index", "target_state", "original_duration"])

TransferCollection = Dict[int, List[PendingTransfer]]


class PendingTransfers:
    def __init__(self):
        self.inner: Dict[int, List[PendingTransfer]] = {}

    def append(self, transfer: PendingTransfer):
        key = transfer.original_duration
        if (extant := self.inner.get(key)) is not None:
            extant.append(transfer)
        else:
            self.inner[key] = [transfer]

    def extend(self, transfers):
        for t in transfers:
            self.append(t)

    def advance(self) -> Sequence[PendingTransfer]:
        # todo improve (rotating array?)
        new_inner = {}
        ret = ()
        for k, v in self.inner.items():
            if k:
                new_inner[k - 1] = v
            else:
                ret = v
        self.inner = new_inner
        return ret


class State(Circle, ABC):
    all_states: List[State] = []

    # todo function to draw a pretty graph

    def __init__(self, name):
        super().__init__("state")
        self.name = name

        self.ancestor: Optional[State] = None
        self.descendant_states: Optional[Dict[str, State]] = {name: self}

        self.ind = len(self.all_states)
        self.all_states.append(self)

    def _add_descendant(self, child: State):
        if self.ancestor:
            self.ancestor._add_descendant(child)
        else:
            self.add_descendant(child)

    def add_descendant(self, child: State):
        if not self.descendant_states:
            raise Exception("cannot indirectly insert a child to a non-root state")
        if self.descendant_states.setdefault(child.name, child) is not child:
            raise Exception(f"duplicate state name {child.name}")
        child.ancestor = self
        child.descendant_states = None

    def __getitem__(self, item: str) -> State:
        if not self.descendant_states:
            raise Exception("cannot index a non-root state")
        return self.descendant_states[item]

    @abstractmethod
    def transfer(self, agents: Collection[Agent]) -> Iterable[PendingTransfer]:
        pass

    def __str__(self):
        return f"<state {self.name}>"


class StochasticState(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.probs = np.array([], dtype=float)
        self.destinations: List[State] = []
        self.durations: List[rv_discrete] = []

    def add_transfer(self, destination: State, duration: Union[rv_discrete, int, Tuple[int, int], Tuple[int, int, int]],
                     probability: Union[float, type(...)]):

        if probability is ...:
            p = 1
        elif self.durations:
            p = self.probs[-1] + probability
            if p > 1:
                raise ValueError("probability higher than 1")
        else:
            p = probability
        # todo improve?
        self.probs = np.append(self.probs, p)

        if isinstance(duration, int):
            duration = rv_discrete(name='const', values=([duration], [1]))()
        if isinstance(duration, tuple):
            if len(duration) == 2:
                duration = randint(*duration)
            elif len(duration) == 3:
                # todo this is super temporary
                a, mid, b = duration
                min_diff = min(mid - a, b - mid)
                a, b = mid - min_diff, mid + min_diff
                duration = randint(a, b)
            else:
                # todo more descriptive
                raise TypeError

        self.destinations.append(destination)
        self.durations.append(duration)

        self._add_descendant(destination)

    def transfer(self, agents: Set[Agent]) -> Iterable[PendingTransfer]:
        transfer_indices = np.searchsorted(self.probs, np.random.random(len(agents)))
        bin_count = np.bincount(transfer_indices)
        durations = [iter(d.rvs(c)) for (c, s, d) in zip(bin_count, self.destinations, self.durations)]
        return [
            PendingTransfer(agent.index, self.destinations[transfer_ind], durations[transfer_ind].__next__())
            for transfer_ind, agent in zip(transfer_indices, agents)
        ]


class TerminalState(State):
    def transfer(self, agents: Set[Agent]) -> Iterable[PendingTransfer]:
        return ()
