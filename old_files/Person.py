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
<<<<<<< HEAD

    def get_age(self):
        if self.age == 1:
            return "kid"
        elif self.age == 2:
            return "teen"
        elif self.age == 3:
            return "adult"
        elif self.age == 4:
            return "old"

    def get_med_state(self):
        if self.med_state == 1:
            return "healthy"
        elif self.med_state == 2:
            return "infected"
        elif self.med_state == 3:
            return "quiet sick"
        elif self.med_state == 4:
            return "low symptoms"
        elif self.med_state == 5:
            return "medium symptoms"
        elif self.med_state == 6:
            return "hard symptoms"
        elif self.med_state == 7:
            return "dead"
        elif self.med_state == 8:
            return "immune"

    def get_social_state(self):
        if self.social_state == 1:
            return "normal"
        elif self.social_state == 2:
            return "no crowds"
        elif self.social_state == 3:
            return "no work/school"
        elif self.social_state == 4:
            return "isolation"
        elif self.social_state == 5:
            return "hospitalization"
        elif self.social_state == 6:
            return "dead"

=======
>>>>>>> a8e0d6f5f22c10efaeb33803614c99fec2426ad1
