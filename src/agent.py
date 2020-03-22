from medical_state import MedicalState, INFECTABLE_MEDICAL_STATES, INFECTIONS_MEDICAL_STATES
import corona_stats


class Agent:
    """
    This class represents a person in our doomed world.
    """
    __slots__ = "ssn", "ID", "home", "work", "medical_state", "infection_date", "is_home_quarantined", "is_full_quarantined"

    def __init__(self, ssn):
        self.ssn = ssn
        self.ID = ssn
        self.home = None
        self.work = None
        self.infection_date = None
        self.medical_state = MedicalState.Healthy
        self.is_home_quarantined = False
        self.is_full_quarantined = False

    def __str__(self):
        return "<Person,  ssn={}, medical={}>".format(self.ssn, self.medical_state)

    def is_infectious(self):
        """
        Check if this agent is infectious.

        :return: bool, True if this agent can infect others.
        """

        # pay attantion, doesn't have to be only in this stage. in the future this could be multiple stages check
        return self.medical_state in INFECTIONS_MEDICAL_STATES

    def is_infectable(self):
        return self.medical_state in INFECTABLE_MEDICAL_STATES

    def infect(self, date=0):
        """
        Will try to infect this agent with given probability
        """
        if self.is_infectable():
            self.change_medical_state(MedicalState.Infected)
            self.infection_date = date
            return True

    def add_home(self, home):
        self.home = home

    def add_work(self, work):
        self.work = work

    def change_medical_state(self, new_status):
        self.medical_state = new_status

    def day_passed(self, roll, current_date):
        if self.infection_date is None or self.infection_date < 0:
            return False
        if current_date >= self.infection_date + corona_stats.average_infection_length:  # todo use random with a given deviation
            if roll < corona_stats.death_ratio:
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
