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
    
    
    def generate_successors(self):
        """Generate a list of successors by swapping elements."""
        successors = []
        i, j, k = 0
        x, y, z = 0, 0, 1
        while i < 4 and j < 4 and k < 4 : 
            successor = Cube(np.copy(self.state))
            successor.swap_two_elements(i, j, k, x, y, z)
            successors.append(successor)
            if (z < 4) :
                z += 1
            elif (y < 4 and z == 4) : 
                y += 1
                z = 0
            elif (y == 4 and z == 4) :
                if (x < 4) :
                    x += 1
                    y = 0
                    z = 0
                else : # x == 4
                    if (k < 4) :
                        k += 1
                    elif (j < 4 and k == 4) :
                        j += 1 
                        k = 0
                    elif (j == 4 and k == 4) :
                        if (i < 4) :
                            j = 0
                            k = 0
                        i += 1
                    x, y, z = i, j, k + 1