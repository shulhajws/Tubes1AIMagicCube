import json
import sys
import time

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

    def climb(self, output_file, max_iterations=1000, max_sideways=50):
        iteration = 0
        sideways = 0

        sys.stdout.write("Loading...\n")
        sys.stdout.flush()

        start_time = time.time()

        while iteration < max_iterations:
            best_successor = self.find_best_successor()

            if best_successor.fitness_value > self.current_cube.fitness_value:
                break
            
            if sideways < max_sideways:
                sideways += 1
                if best_successor.fitness_value == self.current_cube.fitness_value:
                    sideways += 1
                else:
                    sideways = 0
            else:
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

        return self.current_cube, iteration, (finish_time - start_time)
