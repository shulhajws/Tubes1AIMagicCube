import json

class SteepestHillClimb:
    def __init__(self, cube, history=None, initial_iteration=0):
        self.current_cube = cube
        
        if not history:
            self.history = [{
                "iteration": 0,
                "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
                "fitness_value": int(self.current_cube.fitness_value)
            }]
            self.initial_iteration = 0

        else:
            with open("result/"+history, "r") as f:
                self.history = json.load(f)

            self.history.append({
                    "iteration": initial_iteration + 1,
                    "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
                    "fitness_value": int(self.current_cube.fitness_value)
                })
            self.initial_iteration = initial_iteration + 1

    def find_best_successor(self):
        best_successor = None
        best_fitness = float('inf')

        for successor in self.current_cube.generate_successors():
            if successor.fitness_value < best_fitness:
                best_successor = successor
                best_fitness = successor.fitness_value

        return best_successor

    def climb(self, output_file, max_iterations=1000, initial_iteration=0):
        if initial_iteration > 0:
            x = self.initial_iteration + 1
        else:
            x = 1
        
        iteration = 0
        while iteration < max_iterations:
            best_successor = self.find_best_successor()

            if best_successor.fitness_value >= self.current_cube.fitness_value:
                break

            self.current_cube = best_successor

            if output_file is not None:
                self.history.append({
                    "iteration": iteration + x,
                    "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
                    "fitness_value": int(self.current_cube.fitness_value)
                })

                with open("result/"+output_file, "w") as f:
                    json.dump(self.history, f, indent=4)

            print(f"Iteration {iteration+1}: Fitness = {self.current_cube.fitness_value}")

            if self.current_cube.fitness_value == 0:
                break

            iteration += 1

        self.final_iteration = iteration + self.initial_iteration  
        return self.current_cube, iteration
    
    def get_final_iteration(self):
        return self.final_iteration