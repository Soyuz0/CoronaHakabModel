from functools import partial

from medical_state import MedicalState, INFECTABLE_MEDICAL_STATES, INFECTIONS_MEDICAL_STATES
import numpy as np
import corona_stats


def _random_buffer(buffer_size=1024):
    while True:
        yield from np.random.random(buffer_size)


random = partial(next, _random_buffer())


class Agent:
    """
    This class represents a person in our doomed world.
    """
    __slots__ = "ssn", "ID", "home", "work", "medical_state", "infection_date"

    def __init__(self, ssn):
        self.ssn = ssn
        self.ID = ssn
        self.home = None
        self.work = None
        self.infection_date = None
        self.medical_state = MedicalState.Healthy

    def __str__(self):
        return "<Person,  ssn={}, medical={}>".format(self.ssn, self.medical_state)

    def is_infectious(self):
        """
        Check if this agent is infectious.

        :return: bool, True if this agent can infect others.
        """

        # pay attantion, doesn't have to be only in this stage. in the future this could be multiple stages check
        return self.medical_state in INFECTIONS_MEDICAL_STATES

    def infect(self, probability=1, date=0):
        """
        Will try to infect this agent with given probability
        """
        probability = 1 - np.exp(probability)
        if self.is_infectious():
            if random() < probability:
                self.change_medical_state(MedicalState.Infected)
                self.infection_date = date
                return True
        return False

    def add_home(self, home):
        self.home = home

    def add_work(self, work):
        self.work = work

    def change_medical_state(self, new_status):
        self.medical_state = new_status

    def day_passed(self, current_date):
        if self.infection_date is None or self.infection_date < 0:
            return False
        if current_date >= self.infection_date + corona_stats.average_infection_length:  # todo use random with a given deviation
            if random() < corona_stats.death_ratio:
                self.change_medical_state(MedicalState.Deceased)
                return "Dead"
            else:
                self.change_medical_state(MedicalState.Immune)
                return "Recovered"
        return False

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
        rest_of_circle = {o.ID for o in self.agents}
        rest_of_circle.remove(my_index)
        return rest_of_circle
