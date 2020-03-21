import yappi

from manager import SimulationManager


if __name__ == '__main__':
    yappi.stop()
    sm = SimulationManager()
    yappi.start()
    sm.run()