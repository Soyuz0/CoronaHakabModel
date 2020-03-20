import random

import states

class InfectionManager:
    """
    Manages the "Infection" stage of the simulation.
    """
    
    def __init__(self, circles, agents):
        self._circles = circles
        self._agents = agents
    
    def infect_circle(self, circle):
        for agent1 in circle:
            for agent2 in circle:
                if agent1.is_infected():
                    infection_probability = self.calculate_infection_probability(agent1, agent2, circle);
                    self.infect_agent(agent2, infection_probability)
                    
    def calculate_infection_probability(self, agent1, agent2, circle):
        return agent1.infection_rate * circle.density * agent1.relation(agent2.id)
    
    def infect_agent(agent, infection_probability):
        # Get a random number between 0 and 1.
        # If it is smaller than the infection probability, infect the person.
        if random.random() <= infection_probabilty:
            agent.change_health(states.I)
            
    
class InfectionPolicy:
    """
    Holds relevant information about policys that effect infection generaly.
    """
    
    def __init__():
        pass
    
    