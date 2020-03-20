from enum import IntEnum


class Agent:
    """
    This class represents a person in our doomed world.
    """

    def __init__(self, ssn):
        self.ssn = ssn
        self.medical_state = MedicalState.Healthy

    def __str__(self):
        return "<Person,  ssn={}, medical={}>".format(self.ssn, self.medical_state)


class MedicalState(IntEnum):
    Immune = -1
    Healthy = 0
    Infected = 1
    Deceased = 2
