from cube import Cube
from steepest_hill_climb import SteepestHillClimb
from sideways_hill_climb import SidewaysHillClimb
from random_restart_hill_climb import RandomRestartHillClimb
from stochastic_hill_climb import StochasticHillClimb

def main():
    initial_cube = Cube()
    
    print("Initial Cube State:")
    initial_cube.display()
    print("Initial Fitness:", initial_cube.fitness_value)
    
    climber = RandomRestartHillClimb(initial_cube)
    
    result = climber.climb()
    
    print("Final Cube State after Climbing:")
    result.display()
    print("Final Fitness:", result.fitness_value)

if __name__ == "__main__":
    main()
