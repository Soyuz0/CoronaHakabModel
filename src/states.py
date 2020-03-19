import random
from bisect import bisect
from typing import List, Tuple


class State:
    # no slots here, we want each state to be customizable
    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.transition_probs: List[float] = []
        self.transition_dests: List[State] = []

    def add_transition(self, dest, prob):
        next_total = (self.transition_probs[-1] if self.transition_probs else 0) + prob
        if next_total > 1:
            raise ValueError("total transition probabilities cannot exceed 1")
        self.transition_probs.append(next_total)
        self.transition_dests.append(dest)

    def next(self):
        r = random.uniform(0, 1)  # todo better rand
        dest_index = bisect(self.transition_probs, r)
        if dest_index == len(self.transition_probs):
            return None
        return self.transition_dests[dest_index]


class StochasticStateMachine:
    # todo slots

    def __init__(self):
        # the first state introduced is always the initial
        self._state_dict = {}
        self._state_list = []

    def get_state(self, name):
        if ret := self._state_dict.get(name):
            return ret
        ret = State(name, len(self._state_dict))
        self._state_dict[name] = ret
        self._state_list.append(ret)
        return ret

    def __getitem__(self, item) -> State:
        if isinstance(item, int):
            return self._state_list[item]
        return self._state_dict[item]

    # todo render a nice graph with graphviz


HealthMachine = StochasticStateMachine()
S, I, R = HealthMachine["susceptible"], HealthMachine["infected"], HealthMachine["recovered"]
S.infectious = False
I.infectious = False
R.infectious = False

S.add_transition(I, 0.25)
I.add_transition(R, 0.3)
