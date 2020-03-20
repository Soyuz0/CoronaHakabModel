import numpy as np
from scipy.sparse import lil_matrix


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
        self.matrix = lil_matrix((size, size))

        self.m_families = self._create_intra_family_connections()
        self.m_work = self._create_intra_workplace_connections()
        self.m_random = self._create_random_connectivity()

        self.matrix += self.m_families + self.m_work + self.m_random

        self.normalize()

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

        return lil_matrix((self.size, self.size))

    def _create_intra_workplace_connections(self):
        """
        Similar to build the family connections we here build the working place connections
        divide the population which goes to work (say 0.4N) into buckets of size that correspond
        to work place size.
        Within the nodes of each bucket (i.e. each work place), make some random connections according
        to the number of close colleagues each person might have.

        :return: lil_matrix n*n
        """

        return lil_matrix((self.size, self.size))

    def _create_random_connectivity(self):
        """
        plug here random connection, super spreaders, whatever. We can also adjust the number of daily connections
        b or beta in the literature) by adding this random edges
        :return: lil_matrix n*n
        """

        return lil_matrix((self.size, self.size))

    def normalize(self, r0=1.5):
        """
        this funciton should normalize the weights within W to represent the infection rate.
        As r0=bd, where b is number of daily infections per person
        """
        non_zero_elements = sum(np.count_nonzero(v) for v in self.matrix.data)
        b = non_zero_elements / self.size  # average number of connections per person per day
        d = r0 / b
        average_edge_weight_in_matrix = self.matrix.sum() / b
        self.matrix = self.matrix * d / average_edge_weight_in_matrix  # now each entry in W is such that bd=R0

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