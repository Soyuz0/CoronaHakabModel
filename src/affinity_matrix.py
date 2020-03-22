import numpy as np
from scipy.sparse import lil_matrix
from agent import Agent, Circle
import random as rnd
from medical_state import MedicalState, INFECTABLE_MEDICAL_STATES, INFECTIONS_MEDICAL_STATES
import corona_stats, social_stats


class AffinityMAtrix:
    """
    This class builds and maintains the sparse affinity matrix W which describes the social connections
    (the social circles).
    W is NxN, where N is the total population size.
    If W(i,j) is large, this means that node (person) i is socially close to node j.
    Thus, nodes i and j can easly infect one another.
    Naturally, W is symetric.
    """

    def __init__(self, size):
        self.size = size  # population size
        self.matrix = lil_matrix((size, size), dtype=np.float16)

        self.agents = self.generate_agents()

        self.m_families = self._create_intra_family_connections()
        self.m_work = self._create_intra_workplace_connections()
        self.m_random = self._create_random_connectivity()

        self.matrix = self.m_families + self.m_work + self.m_random

        self.normalize()

    def generate_agents(self):
        agents = [Agent(id) for id in range(self.size)]
        return agents

    def _create_intra_family_connections(self):
        """
        here need to build random buckets of size N/self.averageFamilySize
        and add nodes to a NxN sparce amtrix W_famillies describing the connections within each family.
        If for example, nodes 1 till 5 are a family, we need to build connections between each and
        every memeber of this family. The value of each edge should be heigh, representing a
        high chance of passing the virus, since the family members stay a long time together.
        In the example of nodes 1 till 5 buing a family, in Matlab this would be: W_families[1:5,1:5]=p
        where p is the intra family infection probability.
        Late on, if, for example, a policy of house containments takes place without the members of the family
        taking measures to separate from each other, then this value p can be replaced by something even larger.
        """
        # as a beggining, i am making all families the same size, later we will change it to be more sophisticated
        matrix = lil_matrix((self.size, self.size), dtype=np.float16)

        # creating all families, and assigning each agent to a family, and counterwise
        agents_withouth_home = list(range(self.size))
        families = []
        for _ in range(self.size // social_stats.avarage_family_size):
            new_family = Circle("home")
            for _ in range(social_stats.avarage_family_size):
                random_int = rnd.randint(0, len(agents_withouth_home) - 1)
                chosen_agent = self.agents[agents_withouth_home[random_int]]
                agents_withouth_home.remove(agents_withouth_home[random_int])
                chosen_agent.add_home(new_family)
                new_family.add_agent(chosen_agent)
            families.append(new_family)
        self.families = families

        #adding the remaining people to a family (if size % average_family_size != 0)
        if len(agents_withouth_home) > 0:
            new_family = Circle("home")
            for agent_index in agents_withouth_home:
                chosen_agent = self.agents[agent_index]
                chosen_agent.add_home(new_family)
                new_family.add_agent(chosen_agent)
            families.append(new_family)

        # updating the matrix using the families
        for agent in self.agents:
            if agent.home is None:
                continue
            family_members_ids = agent.home.get_indexes_of_my_circle(agent.ID)  # right now families are circle[0]
            for id in family_members_ids:
                matrix[agent.ID, id] = social_stats.family_strength

        return matrix

    def _create_intra_workplace_connections(self):
        """
        Similar to build the family connections we here build the working place connections
        divide the population which goes to work (say 0.4N) into buckets of size that correspond
        to work place size.
        Within the nodes of each bucket (i.e. each work place), make some random connections according
        to the number of close colleagues each person might have.

        :return: lil_matrix n*n
        """
        matrix = lil_matrix((self.size, self.size), dtype=np.float16)

        # creating all families, and assigning each agent to a family, and counterwise
        agents_withouth_work = list(range(self.size))
        works = []
        for _ in range(self.size // social_stats.avarage_work_size):  # todo add last work
            new_work = Circle("work")
            for _ in range(social_stats.avarage_work_size):
                random_int = rnd.randint(0, len(agents_withouth_work) - 1)
                chosen_agent = self.agents[agents_withouth_work[random_int]]
                agents_withouth_work.remove(agents_withouth_work[random_int])
                chosen_agent.add_work(new_work)
                new_work.add_agent(chosen_agent)
            works.append(new_work)
        self.works = works

        # adding the remaining people to a work (if size % average_work_size != 0)
        if len(agents_withouth_work) > 0:
            new_work = Circle("work")
            for agent_index in agents_withouth_work:
                chosen_agent = self.agents[agent_index]
                chosen_agent.add_work(new_work)
                new_work.add_agent(chosen_agent)
            works.append(new_work)

        # updating the matrix using the works
        for agent in self.agents:
            if agent.work is None:
                continue
            work_members_ids = agent.work.get_indexes_of_my_circle(agent.ID)  # right now works are circle[1]
            for id in work_members_ids:
                matrix[agent.ID, id] = social_stats.work_strength

        return matrix

    def _create_random_connectivity(self):
        """
        plug here random connection, super spreaders, whatever. We can also adjust the number of daily connections
        b or beta in the literature) by adding this random edges
        :return: lil_matrix n*n
        """
        matrix = lil_matrix((self.size, self.size), dtype=np.float16)
        for agent in self.agents:
            amount_of_connections = 10  # right now there will be 10 random connections for each agent
            strangers_id = set()
            for _ in range(amount_of_connections):
                strangers_id.add(rnd.randint(0, self.size - 1))
            for id in strangers_id:
                matrix[agent.ID, id] = social_stats.stranger_strength

        return matrix

    def normalize(self):
        """
        this funciton should normalize the weights within W to represent the infection rate.
        As r0=bd, where b is number of daily infections per person
        """
        r0 = corona_stats.r0
        non_zero_elements = sum(np.count_nonzero(v) for v in self.matrix.data)
        b = non_zero_elements / self.size  # average number of connections per person per day
        d = r0 / corona_stats.average_infection_length / b #avarage probability for infection in each meeting as should be
        average_edge_weight_in_matrix = self.matrix.sum() / non_zero_elements #avarage probability for infection in each meeting in current matrix
        self.matrix = self.matrix * d / average_edge_weight_in_matrix # (alpha = d / average_edge_weight_in_matrix) now each entry in W is such that bd=R0
        social_stats.family_strength_not_workers = social_stats.family_strength_not_workers * d / average_edge_weight_in_matrix

        #switching from probability to ln(1-p):
        for row_index in range(self.size):
            row = self.matrix.getrow(row_index)
            for col in row.indices:
                self.matrix[row_index,col] = np.log(1- self.matrix[row_index,col])


    def dot(self, v):
        """
        performs dot operation between this matrix and v
        :param v: with the size of self.size

        :return: matrix*v
        """

        return self.matrix.dot(v)

    def zero_column(col_id):
        """
        Turn the chosen column to zeroes.
        """
        pass
    
    def add_to_column(col_id, col):
        """
        Add the given column to the chosen column
        """
        pass
