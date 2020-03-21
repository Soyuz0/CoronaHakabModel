from enum import IntEnum


class MedicalState(IntEnum):
    Immune = -1
    Healthy = 0
    Infected = 1
    Deceased = 2


INFECTABLE_MEDICAL_STATES = {MedicalState.Healthy}
INFECTIONS_MEDICAL_STATES = {MedicalState.Infected}
IMUNE_MEDICAL_STATES = {MedicalState.Immune, MedicalState.Deceased}