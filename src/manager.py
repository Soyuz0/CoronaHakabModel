from itertools import islice
from affinity_matrix import AffinityMatrix
import logging
import numpy as np
import plotting
import update_matrix
import infection
from consts import Consts
from medical_state import MedicalState
from state_machine import PendingTransfers


class SimulationManager:
    """
    A simulation manager is the main class, it manages the steps performed with policies
    """

    def __init__(self, initial_medical_state: MedicalState, sick_state: MedicalState, consts=Consts()):
        self.consts = consts

        self.pending_transfers = PendingTransfers()

        self.logger = logging.getLogger('simulation')
        logging.basicConfig()
        self.logger.setLevel(logging.INFO)
        self.logger.info("Creating new simulation.")
        self.matrix = AffinityMatrix(self.consts.population_size, consts)
        self.agents = self.matrix.agents

        for agent in self.agents:
            agent.set_medical_state(initial_medical_state)

        self.sick_state = sick_state

        self.stats_plotter = plotting.StatisticsPlotter()
        self.update_matrix_manager = update_matrix.UpdateMatrixManager(self.matrix)
        self.infection_manager = infection.InfectionManager(self)

        self.steps = 0
        self.infectiousness_vector = np.zeros(len(self.agents), dtype=float)

        self.logger.info("Created new simulation.")

    def step(self):
        """
        run one step
        """
        # update matrix
        self.update_matrix_manager.update_matrix_step(self.infection_manager.agents_to_home_quarantine,
                                                      self.infection_manager.agents_to_full_quarantine)

        # update infection
        new_dead, new_recovered = self.infection_manager.infection_step()

        self.steps += 1

        self.stats_plotter.snapshot(self)

    def setup_sick(self):
        """"
        setting up the simulation with a given amount of infected people
        """
        for agent in islice(self.agents, self.consts.initial_infected_count):
            agent.set_medical_state(self.sick_state)

    def generate_policy(self, workers_percent):
        """"
        setting up the simulation with a given amount of infected people
        """
        rolls = np.random.random(len(self.agents))
        for agent, roll in zip(self.agents, rolls):
            if agent.work is None:
                continue
            if roll > workers_percent:
                work_members_ids = agent.work.get_indexes_of_my_circle(agent.index)  # right now works are circle[1]
                for id in work_members_ids:
                    self.matrix.matrix[agent.index, id] = np.log(1)
                family_members_ids = agent.home.get_indexes_of_my_circle(agent.index)  # right now families are circle[0]
                for id in family_members_ids:
                    self.matrix.matrix[agent.index, id] = \
                        np.log(1 - (self.consts.family_strength_not_workers*self.matrix.factor))
        self.setup_sick()

    def run(self):
        """
        runs full simulation
        """
        self.generate_policy(1)
        for i in range(self.consts.total_steps):
            if Consts.active_quarantine:
                if i == self.consts.stop_work_days:
                    self.matrix.change_work_policy(False)
                elif i == self.consts.resume_work_days:
                    self.matrix.change_work_policy(True)
            self.step()
            self.logger.info(
                f"performing step {i + 1}/{self.consts.total_steps}"
            )

    def plot(self):
        self.stats_plotter.plot()

    def __str__(self):
        return "<SimulationManager: SIZE_OF_POPULATION={}, STEPS_TO_RUN={}>".format(self.consts.population_size,
                                                                                    self.consts.total_steps)
