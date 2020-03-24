from manager import SimulationManager
from medical_state import Susceptible, Latent

if __name__ == "__main__":
    sm = SimulationManager(Susceptible, Latent)
    sm.run()
    sm.plot(save=False, max_scale=False)
