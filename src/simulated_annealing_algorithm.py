import math
import json

class SimulatedAnnealing : 
    def __init__(self, cube):
        self.initial_cube = cube
        self.max_iterations = 5000
        self.initial_temperature = 100
        self.history = [{
            "iteration": 0,
            "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
            "fitness_value": int(self.current_cube.fitness_value)
        }]

    def temperature_function(self, iteration) :
        return self.initial_temperature - (0.05 * iteration)

    def probability_function(delta_e, temperature) :
        return math.exp(((-1) * delta_e) / temperature)

    def simulated_annealing_algorithm(self,  threshold, output_file) :
        current_state = self.initial_cube
        i = 0

        while (True and i < self.max_iterations) :
            temperature = SimulatedAnnealing.temperature_function(self, i)
            if (temperature == 0) : 
                return current_state, i
            
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
                    "state": [[row.tolist() for row in layer] for layer in self.current_cube.state],
                    "fitness_value": int(self.current_cube.fitness_value)
                })

                with open("result/"+output_file, "w") as f:
                    json.dump(self.history, f, indent=4)
            
            i += 1
        
        if i == self.max_iterations :
            return current_state, i
        