import json

class SidewaysHillClimb:
    def __init__(self, cube):
        self.current_cube = cube
        self.history = [{
            "iteration": 0,
            "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
            "fitness_value": int(self.current_cube.fitness_value)
        }]

    def find_best_successor(self):
        best_successor = None
        best_fitness = float('inf')

        for successor in self.current_cube.generate_successors():
            if successor.fitness_value < best_fitness:
                best_successor = successor
                best_fitness = successor.fitness_value

        return best_successor

    def climb(self, output_file, max_iterations=1000):
        iteration = 0

        while iteration < max_iterations:
            best_successor = self.find_best_successor()

            if best_successor.fitness_value > self.current_cube.fitness_value:
                break

            self.current_cube = best_successor

            if output_file:
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

            iteration += 1

        return self.current_cube, iteration