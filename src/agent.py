import random
from medical_state import MedicalState, INFECTABLE_MEDICAL_STATES, INFECTIONS_MEDICAL_STATES


class Agent:
    """
    This class represents a person in our doomed world.
    """

    def __init__(self, ssn):
        self.ssn = ssn
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



