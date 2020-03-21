from  affinity_matrix import AffinityMAtrix
import logging
from agent import Agent
import numpy as np
import plotting
import update_matrix


class SimulationManager:
    """
    A simulation manager is the main class, it manages the steps performed with policies
    """

    # GENERAL SIMULATION CONSTS:
    SIZE_OF_POPULATION = 1000
    STEPS_TO_RUN = 20

    def __init__(self):
        self.matrix = AffinityMAtrix(self.SIZE_OF_POPULATION)
        self.agents = self.matrix.agents
        logging.basicConfig()
        self.logger = logging.getLogger('simulation')
        self.logger.setLevel(logging.INFO)
        self.stats_plotter = plotting.StatisticsPlotter()
        self.update_matrix_manager = update_matrix.UpdateMatrixManager()
        
        self.step_counter = 0
        self.infected_per_generation = [0] * self.STEPS_TO_RUN

        self.logger.info("Created new simulation.")

    def _update_matrix(self):
        """
        update matrix using current policies
        """
        # self.update_matrix_manager.update_matrix_step()

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
        
        # Update number of infected (for previous step, to save time)
        num_of_infected = sum(v)
        self.infected_per_generation[self.step_counter] = num_of_infected
        
        u = self.matrix.dot(v)
        for key, value in enumerate(u):
            self.agents[key].infect(value)

    def step(self):
        """
        run one step
        """

        self._update_matrix()
        self._perform_infection()
        
        self.step_counter += 1

    def run(self):
        """
        runs full simulation
        """

        for i in range(self.STEPS_TO_RUN):
            self.step()
            self.logger.info("performing step {}/{} : {} people are infected".format(i, self.STEPS_TO_RUN, self.infected_per_generation[i]))
            
        # plot results
        self.stats_plotter.plot_infected_per_generation(list(map(lambda o: np.log(o),self.infected_per_generation)))

    def __str__(self):
        return "<SimulationManager: SIZE_OF_POPULATION={}, STEPS_TO_RUN={}>".format(self.SIZE_OF_POPULATION,
                                                                                    self.STEPS_TO_RUN)

simulation_manager = SimulationManager()
simulation_manager.run()
