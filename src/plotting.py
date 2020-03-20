from matplotlib import pyplot as plt


class StatisticsPlotter:
    """
    Plots statistics about the simulation.
    """

    def plot_infected_per_generation(self, infected_per_generation_vector):
        plt.plot(infected_per_generation_vector)
        plt.show()


class StatePlotter:
    """
    Plots a current state of the simulation.
    """
    pass
