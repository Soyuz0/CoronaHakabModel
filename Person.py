import numpy as np
import matplotlib as plt


class Person:
    def __init__(self, med_state=1, social_state=1, age=1, checked=False, ssn=1):
        self.age = age
        self.med_state = med_state
        self.social_state = social_state
        self.checked = checked
        self.ssn = ssn

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
            return ""

