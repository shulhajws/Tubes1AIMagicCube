import time
import sys
from cube import Cube
from steepest_hill_climb import SteepestHillClimb

class RandomRestartHillClimb:
    def __init__(self, cube):
        self.initial_cube = cube
        self.best_cube = None
        self.best_fitness = float('inf')

    def climb(self, output_file=None, max_restarts=20, max_iterations=1000):
        iterations_per_restart = []
        fitness_value_per_iteration = {}
        current_iteration = 0

        start_time = time.time()

        for restart in range(max_restarts):
            sys.stdout.write("\rRestart: {}\n".format(restart))
            sys.stdout.flush()
            if restart > 0:
                current_cube = Cube()
                climber = SteepestHillClimb(current_cube, output_file, current_iteration)
            else:
                current_cube = self.initial_cube
                climber = SteepestHillClimb(current_cube)

            result, _, per_iteration, _ = climber.climb(output_file, max_iterations, current_iteration)
            fitness_value_per_iteration[restart+1] = per_iteration
            
            current_iteration = climber.get_final_iteration()
            iterations_per_restart.append([restart+1, current_iteration])

            if result.fitness_value < self.best_fitness:
                self.best_cube = result
                self.best_fitness = result.fitness_value

            if self.best_fitness == 0:
                sys.stdout.write("\033[F" + " " * 50 + "\r")
                break

            sys.stdout.write("\033[F" + " " * 50 + "\r")
        
        finish_time = time.time()

        return self.best_cube, current_iteration, iterations_per_restart, fitness_value_per_iteration, (finish_time - start_time)