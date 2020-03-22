import numpy as np
import plot_stats


class InfectionManager:
    """
    Manages the infection stage
    """
    
    def __init__(self):
        self.agents_to_home_quarantine = []
        self.agents_to_full_quarantine = []
        pass
    
    def infection_step(self, sick_agent_vector, matrix, agents, sick_agents, step_counter):
        # perform infection
        self.agents_to_home_quarantine.clear()
        self.agents_to_full_quarantine.clear()
        self._perform_infection(sick_agent_vector, matrix, agents, sick_agents, step_counter)
        
        # update agents
        new_dead, new_recovered = self._update_sick_agents(sick_agents, sick_agent_vector, step_counter)
        
        return new_dead, new_recovered
    
    def _perform_infection(self, sick_agent_vector, matrix, agents, sick_agents, step_counter):
        """
        perform the infection stage by multiply matrix with infected vector and try to infect agents.

        v = [i for i in self.agents.is_infectious]
        perform w*v
        for each person in v:
            if rand() < v[i]
                agents[i].infect
        """

        v = sick_agent_vector

        u = matrix.matrix.dot(v)
        infections = np.random.random(u.shape) < (1 - np.exp(u))
        for agent, value in zip(agents, infections):
            if value and agent.infect(step_counter):
                sick_agent_vector[agent.ID] = True
                sick_agents.add(agent)
                if plot_stats.home_quarantine_sicks and np.random.random() < plot_stats.precents_of_caught_sicks: #todo switch to a specific distribution
                    self.agents_to_home_quarantine.append(agent)
                if plot_stats.full_quarantine_sicks and np.random.random() < plot_stats.precents_of_caught_sicks:
                    self.agents_to_full_quarantine.append(agent)

                
    def _update_sick_agents(self, sick_agents, sick_agent_vector, step_counter):
        """
        after each day, go through all sick agents and updates their status (allowing them to recover or die)
        """
        # return parameters
        new_dead = 0
        new_recovered = 0
        
        to_remove = set()
        rolls = np.random.random(len(sick_agents))
        for agent, roll in zip(sick_agents, rolls):
            result = agent.day_passed(roll, step_counter)
            if result:
                to_remove.add(agent)
                sick_agent_vector[agent.ID] = False
                if result == "Dead":
                    new_dead = new_dead + 1
                elif result == "Recovered":
                    new_recovered = new_recovered + 1
        sick_agents.difference_update(to_remove)
        
        return new_dead, new_recovered