from scipy.sparse import lil_matrix

# This class builds and maintains the sparse affinity matrix W which describes the social connections
# (the social circles).
# W is NxN, where N is the total population size.
# If W(i,j) is large, this means that node (person) i is socially close to node j.
# Thus, nodes i and j can easly infect one another.
# Naturally, W is symetric.

AVERAGE_FAMILY_SIZE = 5
self.averageConnectionsAtWorkPlace = 10
self.randomContacts = 20  # but better if we could later on draw this number randomly for each person, from an exponential distribution
DAYS_TO_RUN = 30
POPOLUTION_NUMBER = 9000000

class AffinityMAtrix:
    def __init__(self, size):
        self.size = size  # population size
        self.matrix = lil_matrix((size, size))
        # Now just plugging in some numbers to reprenst the average bucket size for each social connection type:

        self.m_families = self._createIntraFamilyConnections()
        self.m_work = self._createIntraWorkPlaceConnections()
        self.m_random = self._createRandomConnectivity()

        self.matrix += self.m_families + self.m_work + self.m_random

        self.normalize()

    def _createIntraFamilyConnections(self):
        # here need to build random buckets of size N/self.averageFamilySize
        # and add nodes to a NxN sparce amtrix W_famillies describing the connections within each family.
        # If for example, nodes 1 till 5 are a family, we need to build connections between each and
        # every memeber of this family. The value of each edge should be heigh, representing a
        # high chance of passing the virus, since the family members stay a long time together.
        # In the example of nodes 1 till 5 buing a family, in Matlab this would be: W_families[1:5,1:5]=p
        # where p is the intra family infection probability.
        # Late on, if, for example, a policy of house containments takes place without the members of the family
        # taking measures to separate from each other, then this value p can be replaced by something even larger.
        return lil_matrix((self.size, self.size))

    def _createIntraWorkPlaceConnections(self):
        # Similar to build the family connections we here build the working place connections
        # divide the population which goes to work (say 0.4N) into buckets of size that correspond
        # to work place size.
        # Within the nodes of each bucket (i.e. each work place), make some random connections according
        # to the number of close colleagues each person might have.
        return lil_matrix((self.size, self.size))

    def _createRandomConnectivity(self):
        # plug here random connection, super spreaders, whatever. We can also adjust the number of daily connections
        #  (b or beta in the literature) by adding this random edges
        return lil_matrix((self.size, self.size))


    def normalize(self, r0=1.5):
        # this funciton should normalize the weights within W to represent the infection rate.
        # As r0=bd, where b is number of daily

        #b = numberOfNoneZeroElemntsInW / self.N  # average number of connections per person per day
        #d = R0 / b  # average infection probability of each contact
        #averageEdgeWeighInW = sumOfValuesInW / numberOfNoneZeroElemntsInW
        #self.matrix = self.matrix * d / averageEdgeWeighInW  # now each entry in W is such that bd=R0
        return self.matrix




def PropagateDailyConnections(v):
    # Let v be a Nx1 vector, containing the records of who is currently infecting;
    # (if, say, v[i]==1 this means node i is currently infectios, and if v[i]==0 he is not).
    # Then Wv is the probabilty of inefction of each person after one day
    return W * v




def main():
    w = AffinityMAtrix()
    v = make_some_random_vector_of_zeros_and_ones_of
    length_N  # initial infectios condition
    for day in xrange(DAYS_TO_RUN):
        v = W.PropagateDailyConnections()
        v = DefineStateOfEachNode(v)  # Here we need to define the current health of each person.
        # so, if for example v=W.PropagateDailyConnections() returned within entry v[10] the value 0.5
        # this means that person number 10 has 50% chance of being infected.
        # We can now apply a markov model to v[10] according to the SIR model for starts.
        # This means that if v[10] was already in the Recovered state then him being infected means
        # nothing, and the funciton returns v[10]=0 (since this persion is no longer infectios).
        # If, however, this node was susceptible he can ineed move to the infected state with probability 50%
        # and if that happens, the function will return v[10]=1 (i.e this person might now infect others)
