from visualizer import plot_cube_state

class SteepestHillClimb:
    def __init__(self, cube):
        self.current_cube = cube

    def find_best_successor(self):
        best_successor = self.current_cube
        best_fitness = self.current_cube.fitness_value

        for successor in self.current_cube.generate_successors():
            if successor.fitness_value < best_fitness:
                best_successor = successor
                best_fitness = successor.fitness_value

        return best_successor

    def climb(self, max_iterations=1000):
        for iteration in range(max_iterations):
            best_successor = self.find_best_successor()

            if best_successor.fitness_value >= self.current_cube.fitness_value:
                break

            self.current_cube = best_successor
            plot_cube_state(self.current_cube, iteration)
            print(f"Iteration {iteration+1}: Fitness = {self.current_cube.fitness_value}")

        return self.current_cube
