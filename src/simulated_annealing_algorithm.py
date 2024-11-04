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

    def temperature_function(self, choice, iteration) :
        result = 0
        if (choice == 1) :
            result = self.initial_temperature / (1 + 0.05 * iteration * iteration)
        elif (choice == 2) :
            result  = self.initial_temperature - (0.05 * iteration)
        elif (choice == 3) :
            result = self.initial_temperature / (1 + 0.05 * math.log(iteration + 1))
        elif (choice == 4) :
            result = self.initial_temperature * math.pow(0.05, iteration)
        else : 
            result = self.initial_temperature / (1 + 0.05 * iteration * iteration)
        return result

    def probability_function(delta_e, temperature) :
        return math.exp(((-1) * delta_e) / temperature)

    def simulated_annealing_algorithm(self,  threshold, output_file) :
        current_state = self.initial_cube
        i = 0

        print("Choose cooling schedule you want to use from options below!\n1. Default (Quadratic Multiplicative Monotonic)\n2. Linear Multiplicative Monotonic\n3. Logarithmic Multiplicative\n4. Exponential Multiplicative Monotonic")
        temp_function_choice = int(input("Input your choice (1-4) : "))
        print("")

        while (True and i < self.max_iterations) :
            temperature = SimulatedAnnealing.temperature_function(self, temp_function_choice, i)
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
        