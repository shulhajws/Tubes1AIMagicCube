import math
import json
import sys
import time

class SimulatedAnnealing : 
    def __init__(self, cube):
        self.initial_cube = cube
        self.max_iterations = 5000
        self.initial_temperature = 100
        self.history = [{
            "iteration": 0,
            "state": [[row.tolist() for row in layer] for layer in self.initial_cube.state],
            "fitness_value": int(self.initial_cube.fitness_value)
        }]

    def temperature_function(self, iteration) :
        return self.initial_temperature - (0.05 * iteration)

    def probability_function(delta_e, temperature) :
        return math.exp(((-1) * delta_e) / temperature)

    def simulated_annealing_algorithm(self,  threshold, output_file) :
        current_state = self.initial_cube
        i = 0

        sys.stdout.write("Loading...\n")
        sys.stdout.flush()

        start_time = time.time()

        while (True and i < self.max_iterations) :
            temperature = SimulatedAnnealing.temperature_function(self, i)
            if (temperature == 0) :
                finish_time = time.time()

                return current_state, i, (finish_time - start_time)
            
            neighbor = current_state.find_random_successor()

            state_value_difference = neighbor.calculate_fitness() - current_state.calculate_fitness()

            if state_value_difference < 0 :
                current_state = neighbor
            else : 
                if (SimulatedAnnealing.probability_function(state_value_difference, temperature) >= threshold) :
                    current_state = neighbor
            
            if output_file:
                self.history.append({
                    "iteration": i + 1,
                    "state": [[row.tolist() for row in layer] for layer in current_state.state],
                    "fitness_value": int(current_state.fitness_value)
                })

                with open("result/"+output_file, "w") as f:
                    json.dump(self.history, f, indent=4)
            
            if i % 100 == 0:
                sys.stdout.write("\rCurrent iteration: {}".format(i))
                sys.stdout.flush()
                time.sleep(0.1)
            
            i += 1

        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.write("\033[F" + " " * 50 + "\r")
        finish_time = time.time()

        return current_state, i, (finish_time - start_time)
        