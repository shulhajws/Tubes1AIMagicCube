class StochasticHillClimb:
    def __init__(self, cube):
        self.current_cube = cube

    def climb(self, max_iterations=1000):
        for i in range(max_iterations):
            successor = self.current_cube.find_random_successor()

            if successor.fitness_value < self.current_cube.fitness_value:
                self.current_cube = successor

            print(f"Iteration {i+1}: Fitness = {self.current_cube.fitness_value}")

        return self.current_cube