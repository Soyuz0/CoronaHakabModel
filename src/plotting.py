from matplotlib import pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

class StatisticsPlotter:
    """
    Plots statistics about the simulation.
    """

    def plot_infected_per_generation(self, infected_per_generation_vector):
        plt.plot(infected_per_generation_vector)
        plt.show()

    
    def plot_log_with_linear_regression(self, infected_per_generation_vector):
        # fit only to the start of the model.
        # We will always start with exponent, then die down one way or another.
        diff_vector = np.diff(infected_per_generation_vector)
        x_start_search = np.argmax(diff_vector > 0)
        x_max = np.argmax(diff_vector[x_start_search:] <= 0) # fit only until curvature starts going down.
        
        # get log vector
        log_vector = np.log(infected_per_generation_vector)
        
        # put into variables for the fitting
        orig_x = np.array(range(log_vector.size))
        x = orig_x[:x_max].reshape((-1, 1)) # used for the regression
        y = log_vector[:x_max]
        
        # fit to linear
        model = LinearRegression()
        model.fit(x, y)
        
        # get fitting constants, y = b0 + b1*X
        b_0 = model.intercept_
        b_1 = model.coef_[0]
        r_sqr = model.score(x, y) # R^2
        
        # plot the regression line
        regression_x = np.linspace(0,x_max,100)
        regression_y = b_1 * regression_x + b_0
        plt.plot(regression_x, regression_y, '-r',
            label="{:.2f} + {:.2f}*x; R^2 = {:.2f}".format(b_0, b_1, r_sqr))
        
        # plot the data itself
        plt.plot(orig_x,log_vector)
        
        # plot parameters
        plt.title('Log graph with regression')
        plt.xlabel('x', color='#1C2833')
        plt.ylabel('y', color='#1C2833')
        plt.legend(loc='upper left')
        plt.grid()
        
        plt.show()
        


class StatePlotter:
    """
    Plots a current state of the simulation.
    """
    pass

