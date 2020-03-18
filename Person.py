from enum import IntEnum
from typing import Union

import numpy as np
import matplotlib as plt


class AgeCategory(IntEnum):
    Kid = 0
    Teen = 1
    Adult = 2
    Old = 3


class MedicalState(IntEnum):
    Immune = -1
    Healthy = 0
    Infected = 1
    Asymptomatic = 2
    SymptomaticLow = 3
    SymptomaticMedium = 4
    SymptomaticHigh = 5
    Deceased = 6


class SocialState(IntEnum):
    Normal = 0
    NoCrowd = 1
    NoRoutine = 2
    Other = 3


class Person:
    def __init__(self, med_state: Union[int, MedicalState] = 0, social_state: Union[int, SocialState] = 0,
                 age: Union[int, AgeCategory] = 0, checked=False, ssn=1):
        self.age = AgeCategory(age)
        self.med_state = MedicalState(med_state)
        self.social_state = SocialState(social_state)
        self.checked = checked
        self.ssn = ssn
