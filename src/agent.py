import random
from medical_state import MedicalState, INFECTABLE_MEDICAL_STATES, INFECTIONS_MEDICAL_STATES

class Agent:
    """
    This class represents a person in our doomed world.
    """
    __slots__ = "ID", "health_status", "home", "work"
    def __init__(self, ssn):
        self.ssn = ssn
        self.ID = ssn
        self.home = None
        self.work = None
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

    def infect(self, probability=1):
        """
        Will try to infect this agent with given probability
        """
        if self.medical_state in INFECTABLE_MEDICAL_STATES:
            if random.random() < probability:
                self.medical_state = MedicalState.Infected
                
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
