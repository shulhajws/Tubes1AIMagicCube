import json
import sys
import time

class StochasticHillClimb:
    def __init__(self, cube):
        self.current_cube = cube
        self.history = [{
            "iteration": 0,
            "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
            "fitness_value": int(self.current_cube.fitness_value)
        }]

    def climb(self, output_file, max_iterations=1000):
        iteration = 0

        sys.stdout.write("Loading...\n")
        sys.stdout.flush()

        start_time = time.time()
                
        while iteration < max_iterations:
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