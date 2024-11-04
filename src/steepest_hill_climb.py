import json
import sys
import time

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
        
        sys.stdout.write("Loading...\n")
        sys.stdout.flush()

        start_time = time.time()

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

            if self.current_cube.fitness_value == 0:
                break
            
            if iteration % 10 == 0:
                sys.stdout.write("\rCurrent iteration: {}".format(iteration))
                sys.stdout.flush()
                time.sleep(0.1)

            iteration += 1

        finish_time = time.time()
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.write("\033[F" + " " * 50 + "\r")

        self.final_iteration = iteration + self.initial_iteration  
        return self.current_cube, iteration, (finish_time - start_time)
    
    def get_final_iteration(self):
        return self.final_iteration