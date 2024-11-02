import numpy as np
from objective_function import objective_function

class Cube:
    def __init__(self, state=None):
        self.state = state if state is not None else np.random.permutation(np.arange(1, 126)).reshape(5, 5, 5)
        self.fitness_value = self.calculate_fitness()
    
    def calculate_fitness(self):
        """Calculate and update the fitness value using the imported function."""
        return objective_function(self.state)
    
    def display(self):
        """Print each layer of the cube for visualization."""
        for i in range(5):
            print(f"Layer {i + 1}:\n{self.state[i]}\n")

    def swap_two_elements(self, i, j, k, x, y, z): 
        """Swap two elements in the cube state."""
        self.state[i, j, k], self.state[x, y, z] = self.state[x, y, z], self.state[i, j, k]
        self.fitness_value = self.calculate_fitness()