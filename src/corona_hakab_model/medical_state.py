from abc import ABC

from state_machine import State, StochasticState, TerminalState


class MedicalState(State, ABC):
    infectable: bool
    infectiousness: float


class InfectableState(MedicalState, ABC):
    infectable = True
    infectiousness = 0


class InfectiousState(MedicalState, ABC):
    infectable = False

    def __init__(self, *args, infectiousness: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.infectiousness = infectiousness


class ImmuneState(MedicalState, ABC):
    infectable = False
    infectiousness = 0


class InfectableTerminalState(InfectableState, TerminalState):
    pass


class ImmuneStochasticState(ImmuneState, StochasticState):
    pass


class InfectiousStochasticState(InfectiousState, StochasticState):
    pass


class ImmuneTerminalState(ImmuneState, TerminalState):
    pass


Susceptible = InfectableTerminalState("Susceptible")
Latent = ImmuneStochasticState("Latent")
Silent = InfectiousStochasticState("Silent", infectiousness=0.1)
Symptomatic = InfectiousStochasticState("Symptomatic", infectiousness=0.5)
Asymptomatic = InfectiousStochasticState("Asymptomatic", infectiousness=0.3)

Hospitalized = InfectiousStochasticState("Hospitalized", infectiousness=0.5)
ICU = InfectiousStochasticState("ICU", infectiousness=0.5)

Deceased = ImmuneTerminalState("Deceased")
Recovered = ImmuneTerminalState("Recovered")

Susceptible.add_descendant(Silent)
Latent.add_transfer(Silent, (1, 3), ...)

Silent.add_transfer(Asymptomatic, (0, 3, 10), 0.2)
Silent.add_transfer(Symptomatic, (0, 3, 10), ...)

Symptomatic.add_transfer(Asymptomatic, (7, 10, 14), 0.85)
Symptomatic.add_transfer(Hospitalized, 1, ...)

Hospitalized.add_transfer(ICU, 5, 0.2)
Hospitalized.add_transfer(Asymptomatic, 18, ...)

ICU.add_transfer(Hospitalized, 1, 0.65)
ICU.add_transfer(Deceased, 7, 0.35)

Asymptomatic.add_transfer(Recovered, (3, 5, 7), ...)
