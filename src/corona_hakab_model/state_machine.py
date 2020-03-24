from __future__ import annotations

from abc import ABC, abstractmethod
from collections import namedtuple
from typing import List, Dict, Set, Optional, Iterable, Collection, Union, Tuple, Sequence, Generic, TypeVar

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

    def __init__(self, name):
        super().__init__("state")
        self.name = name

        self.machine: Optional[StateMachine] = None

        self.ind = len(self.all_states)
        self.all_states.append(self)

    def _add_descendant(self, child: State):
        self.machine.add_state(child)

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


T = TypeVar('T', bound=State)


class StateMachine(Generic[T]):
    def __init__(self, initial_state: T):
        self.initial: T = initial_state
        self.states = {initial_state.name: initial_state}

    def __getitem__(self, item: Union[str, Tuple[str, ...]]):
        if isinstance(item, str):
            return self.states[item]
        return (self[i] for i in item)

    def add_state(self, state: T):
        if self.states.setdefault(state.name, state) is not state:
            raise Exception(f"duplicate state name {state.name}")
        state.machine = self

    # todo function to draw a pretty graph