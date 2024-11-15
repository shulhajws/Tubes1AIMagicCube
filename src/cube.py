import numpy as np
import random
import time
from objective_function import objective_function_latest  # Updated import for latest function

class Cube:
    def __init__(self, state=None):
        # Initialize state and other attributes
        self.state = state if state is not None else np.random.permutation(np.arange(1, 126)).reshape(5, 5, 5)
        self.switched_coordinate = None
        self.fitness_value, self.best_lines, self.worst_lines = self.calculate_fitness()  # Now captures best/worst lines

    def calculate_fitness(self):
        # Update this method to return best and worst lines as well
        fitness_value, best_lines, worst_lines = objective_function_latest(self.state)
        return fitness_value, best_lines, worst_lines  

    def display(self):
        for i in range(5):
            time.sleep(0.5)
            print(f"Layer {i + 1}:\n{self.state[i]}\n")

    def swap_two_elements(self, i, j, k, x, y, z):
        # Swap elements and recalculate fitness (including best/worst lines)
        self.state[i, j, k], self.state[x, y, z] = self.state[x, y, z], self.state[i, j, k]
        self.fitness_value, self.best_lines, self.worst_lines = self.calculate_fitness()

    def generate_successors(self):
        successors = []
        i, j, k = 0, 0, 0
        x, y, z = 0, 0, 1

        while i < 4 and j < 4 and k < 4 : 
            if ((x, y, z, i, j, k) != self.switched_coordinate) :
                successor = Cube(np.copy(self.state))
                successor.swap_two_elements(i, j, k, x, y, z)
                successor.switched_coordinate = (i, j, k, x, y, z)
                successors.append(successor)
            if z < 4:
                z += 1
            elif y < 4 and z == 4:
                y += 1
                z = 0
            elif y == 4 and z == 4:
                if x < 4:
                    x += 1
                    y = 0
                    z = 0
                else:  # x == 4
                    if k < 4:
                        k += 1
                    elif j < 4 and k == 4:
                        j += 1
                        k = 0
                    elif j == 4 and k == 4:
                        if i < 4:
                            j = 0
                            k = 0
                        i += 1
                    x, y, z = i, j, k + 1

        return successors

    def find_random_successor(self):
        i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        while (i1, j1, k1) == (i2, j2, k2):
            i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        successor = Cube(np.copy(self.state))
        successor.swap_two_elements(i1, j1, k1, i2, j2, k2)

        return successor
