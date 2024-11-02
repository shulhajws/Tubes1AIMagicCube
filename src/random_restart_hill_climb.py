from cube import Cube
from steepest_hill_climb import SteepestHillClimb

class RandomRestartHillClimb:
    def __init__(self, cube, max_restarts=10, max_iterations=1000):
        self.initial_cube = cube
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
        self.best_cube = None
        self.best_fitness = float('inf')

    def climb(self):
        for restart in range(self.max_restarts):
            if restart > 0:
                current_cube = Cube()
            else:
                current_cube = self.initial_cube
            climber = SteepestHillClimb(current_cube)

            result = climber.climb(max_iterations=self.max_iterations)

            if result.fitness_value < self.best_fitness:
                self.best_cube = result
                self.best_fitness = result.fitness_value

            print(f"Restart {restart + 1}: Fitness = {result.fitness_value}")

            if self.best_fitness == 0:
                print("Perfect solution found.")
                break

        return self.best_cube