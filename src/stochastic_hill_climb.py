import json

class StochasticHillClimb:
    def __init__(self, cube):
        self.current_cube = cube
        self.history = [{
            "iteration": 0,
            "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
            "fitness_value": int(self.current_cube.fitness_value)
        }]

    def climb(self, output_file, max_iterations=1000):
        for iteration in range(max_iterations):
            neighbor = self.current_cube.find_random_successor()

            if neighbor.fitness_value < self.current_cube.fitness_value:
                self.current_cube = neighbor
            
            if output_file is not None:
                self.history.append({
                    "iteration": iteration + 1,
                    "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
                    "fitness_value": int(self.current_cube.fitness_value)
                })

                with open("result/"+output_file, "w") as f:
                    json.dump(self.history, f, indent=4)

            print(f"Iteration {iteration+1}: Fitness = {self.current_cube.fitness_value}")

            if self.current_cube.fitness_value == 0:
                break

        return self.current_cube, iteration