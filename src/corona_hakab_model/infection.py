import numpy as np

import manager


class InfectionManager:
    """
    Manages the infection stage
    """

    def __init__(self, sim_manager: 'manager.SimulationManager'):
        self.agents_to_home_quarantine = []
        self.agents_to_full_quarantine = []
        self.manager = sim_manager

    def infection_step(self):
        # perform infection
        self.agents_to_home_quarantine.clear()
        self.agents_to_full_quarantine.clear()
        return self._perform_infection()

    def _perform_infection(self):
        """
        perform the infection stage by multiply matrix with infected vector and try to infect agents.

        v = [i for i in self.agents.is_infectious]
        perform w*v
        for each person in v:
            if rand() < v[i]
                agents[i].infect
        """

        v = np.random.random(len(self.manager.agents)) < self.manager.infectiousness_vector

        u = self.manager.matrix.matrix.dot(v)
        infections = np.random.random(u.shape) < (1 - np.exp(u))
        caught_rolls = np.random.random(u.shape) < self.manager.consts.caught_sicks_ratio
        new_infected = []
        for agent, value, caught_roll in zip(self.manager.agents, infections, caught_rolls):
            if value and agent.medical_state.infectable:
                new_infected.append(agent)
                agent.set_medical_state(self.manager.sick_state)
                if caught_roll:
                    if self.manager.consts.home_quarantine_sicks:
                        self.agents_to_home_quarantine.append(agent)
                    elif self.manager.consts.full_quarantine_sicks:
                        self.agents_to_full_quarantine.append(agent)

        return new_infected
