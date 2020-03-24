from enum import IntEnum


class MedicalState(IntEnum):
    Immune = -1
    Healthy = 0
    Latent = 1
    Silent = 2
    Asymptomatic = 3
    Symptomatic = 4
    Hospitalized = 5
    Icu = 6
    Deceased = 7


INFECTABLE_MEDICAL_STATES = {MedicalState.Healthy}
INFECTIONS_MEDICAL_STATES = {
    MedicalState.Asymptomatic,
    MedicalState.Symptomatic,
    MedicalState.Hospitalized,
    MedicalState.Icu,
}
IMUNE_MEDICAL_STATES = {MedicalState.Immune, MedicalState.Deceased}
