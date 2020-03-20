from  affinity_matrix import AffinityMAtrix
import logging
from agent import Agent
import numpy as np


class SimulationManager:
    """
    A simulation manager is the main class, it manages the steps performed with policies
    """

    # GENERAL SIMULATION CONSTS:
    SIZE_OF_POPULATION = 1000
    STEPS_TO_RUN = 100

    def __init__(self):
        self.matrix = AffinityMAtrix(self.SIZE_OF_POPULATION)
        self.agents = [Agent(i) for i in xrange(self.SIZE_OF_POPULATION)]
        self.logger = logging.getLogger('simulation')
        self.logger.setLevel(logging.INFO)

        self.logger.info("Created new simulation.")

    def _update_matrix(self):
        """
        update matrix using current policies
        """
        pass

    def _perform_infection(self):
        """
        perform the infection stage by multiply matrix with infected vector and try to infect agents.

        v = [i for i in self.agents.is_infectious]
        perform w*v
        for each person in v:
            if rand() < v[i]
                agents[i].infect
        """

        v = np.array([agent.is_infectious() for agent in self.agents])
        u = self.matrix.dot(v)
        for key, value in enumerate(u):
            self.agents[key].infect(value)

    def step(self):
        """
        run one step
        """

        self._update_matrix()
        self._perform_infection()


    def run(self):
        """
        runs full simulation
        """

        for i in xrange(sm.STEPS_TO_RUN):
            self.logger.info("performing step {}/{}".format(i, self.STEPS_TO_RUN))
            self.step()

    def __str__(self):
        return "<SimulationManager: SIZE_OF_POPULATION={}, STEPS_TO_RUN={}>".format(self.SIZE_OF_POPULATION,
                                                                                    self.STEPS_TO_RUN)


if __name__ == '__main__':
    sm = SimulationManager()
    sm.run()

