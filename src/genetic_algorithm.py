import random
from cube import Cube,np

def roulette_wheel_selection(population):
    """Select a parent from the population using roulette wheel selection based on fitness."""
    total_fitness = sum(cube.fitness_value for cube in population)
    relative_fitness = [round(cube.fitness_value * 100 / total_fitness, 3) for cube in population]
    cumulative_probabilities = np.cumsum(relative_fitness)

    # print(f"total_fitness: {total_fitness}\n")
    # print(f"relative_fitness: {relative_fitness}\n")
    # print(f"cumulative_probabilities: {cumulative_probabilities}\n")

    rand = random.random() * 100
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if rand <= cumulative_probability:
            # print(f"rand: {rand}")
            # print(f"cumulative: {cumulative_probability}")
            return population[i]
    return population[-1]

def initialize_population(population_size):
    """Initialize a population of Cube objects with random states."""
    return [Cube() for _ in range(population_size)]

def crossover_optimized(parent1, parent2):
    """partially mapped crossover """
    child1 = np.copy(parent1.state)
    child2 = np.copy(parent2.state)

    # PMX mappings for the area
    mapping1 = {}
    mapping2 = {}
    crossover_index_parent1 = []
    crossover_index_parent2 = []

    # crossover will be performed on child1 by "replacing" the parent1's worstline with parent2's bestline
    for crossover_idx in range(3):
        # Replace in child1 using parent2's best line
        worst_line_indices_parent1 = parent1.worst_lines[crossover_idx][1]
        best_line_indices_parent2 = parent2.best_lines[crossover_idx][1]

        if worst_line_indices_parent1[2] == -1:  # worst line is a row
            for k in range(5):
                ori_val = child1[worst_line_indices_parent1[0], worst_line_indices_parent1[1], k]
                child1[worst_line_indices_parent1[0], worst_line_indices_parent1[1], k] = parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]
                crossover_index_parent1.append((worst_line_indices_parent1[0], worst_line_indices_parent1[1], k))
                # if (ori_val != parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]):
                mapping1[ori_val] = parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]
                mapping2[parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]] = ori_val
                    

        elif worst_line_indices_parent1[1] == -1:  # worst line is a column
            for j in range(5):
                ori_val = child1[worst_line_indices_parent1[0], j, worst_line_indices_parent1[2]]
                child1[worst_line_indices_parent1[0], j, worst_line_indices_parent1[2]] = parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]
                crossover_index_parent1.append((worst_line_indices_parent1[0], j, worst_line_indices_parent1[2]))
                # if (ori_val != parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]):
                mapping1[ori_val] = parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]
                mapping2[parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]] = ori_val

        elif worst_line_indices_parent1[0] == -1:  # Best line is a pillar
            for i in range(5):
                ori_val = child1[i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]]
                child1[i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]] = parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]
                crossover_index_parent1.append((i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]))
                # if (ori_val != parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]):
                mapping1[ori_val] = parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]
                mapping2[parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]] = ori_val
                    
        if best_line_indices_parent2[2] == -1:  # Best line is a row
            for l in range(5):
                ori_val = child2[best_line_indices_parent2[0], best_line_indices_parent2[1], l]
                child2[best_line_indices_parent2[0], best_line_indices_parent2[1], l] =  parent1.state[worst_line_indices_parent1[0], worst_line_indices_parent1[1], l]
                crossover_index_parent2.append((best_line_indices_parent2[0], best_line_indices_parent2[1], l))
                # if (ori_val != parent1.state[worst_line_indices_parent1[0], worst_line_indices_parent1[1], l]):
                    

        elif best_line_indices_parent2[1] == -1:  # Best line is a column
            for m in range(5):
                ori_val = child2[best_line_indices_parent2[0], m, best_line_indices_parent2[2]]
                child2[best_line_indices_parent2[0], m, best_line_indices_parent2[2]] = parent1.state[worst_line_indices_parent1[0], m, worst_line_indices_parent1[2]]
                crossover_index_parent2.append((best_line_indices_parent2[0], m, best_line_indices_parent2[2]))
                # if (ori_val != parent1.state[worst_line_indices_parent1[0], m, worst_line_indices_parent1[2]]):
                # mapping2[ori_val] = parent1.state[worst_line_indices_parent1[0], m, worst_line_indices_parent1[2]]
                        

        elif best_line_indices_parent2[0] == -1:  # Best line is a pillar
            for n in range(5):
                ori_val = child2[n, best_line_indices_parent2[1], best_line_indices_parent2[2]] 
                child2[n, best_line_indices_parent2[1], best_line_indices_parent2[2]] = parent1.state[n, worst_line_indices_parent1[1], worst_line_indices_parent1[2]]
                crossover_index_parent2.append((n, best_line_indices_parent2[1], best_line_indices_parent2[2]))
                # if (ori_val != parent1.state[i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]]):
                # mapping2[ori_val] = parent1.state[n, worst_line_indices_parent1[1], worst_line_indices_parent1[2]]
                    
    print(mapping1)
    print(crossover_index_parent1)
    print(mapping2)
    print(crossover_index_parent2)
    # print(crossover_index_parent1)

    # Resolve conflicts in child
    for row in range(5):
        for col in range(5):
            for pilar in range(5):
                if not ((row, col, pilar) in crossover_index_parent1):
                    original_value_child1 = child1[row, col, pilar]
                    while original_value_child1 in mapping1:
                        original_value_child1 = mapping1[original_value_child1]
                    child1[row, col, pilar] = original_value_child1

                if not ((row, col, pilar) in crossover_index_parent2):          
                    original_value_child2 = child2[row, col, pilar]
                    while original_value_child2 in mapping2:
                        original_value_child2 = mapping2[original_value_child2]
                    child2[row, col, pilar] = original_value_child2
                
    # Return new Cube objects as children
    return Cube(child1), Cube(child2)

# def crossover(parent1, parent2):
#     layer=[0,1,2,3,4]
#     """partially mapped crossover """
#     child1 = np.copy(parent1.state)
#     child2 = np.copy(parent2.state)

#     # PMX mappings for the area
#     mapping1 = {}
#     mapping2 = {}

#     # Choose crossover points within the layer
#     row_start, row_end = 2,4
#     col_start, col_end = 2,4
    
#     # Create mappings and swap values within the crossover region
#     for i in layer:
#         for j in range(row_start, row_end + 1):
#             for k in range(col_start, col_end + 1):
#                 val1 = parent1.state[i, j, k]
#                 val2 = parent2.state[i, j, k]
                
#                 # if val1 != val2:
#                     # Swap values in the crossover region
#                 child1[i, j, k] = val2
#                 child2[i, j, k] = val1
                
#                 # Create mappings for conflict resolution
#                 mapping1[val2] = val1
#                 mapping2[val1] = val2 

#     # print("mapping 2")
#     # print(mapping2)
    
#     # # Resolve conflicts in child
#     for i in range(5):
#         for j in range(5):
#             for k in range(5):
#                 # print(i in layer)
#                 if not ((i in layer) and (row_start <= j <= row_end) and (col_start <= k <= col_end)):
#                     original_value_child1 = child1[i, j, k]
#                     while original_value_child1 in mapping1:
#                         original_value_child1 = mapping1[original_value_child1]
#                     child1[i, j, k] = original_value_child1

#                     original_value_child2 = child2[i, j, k]
#                     while original_value_child2 in mapping2:
#                         original_value_child2 = mapping2[original_value_child2]
#                     child2[i, j, k] = original_value_child2
                
#     # Return new Cube objects as children
#     return Cube(child1), Cube(child2)

def mutate(state):
    """Mutate a cube state by randomly swapping two elements."""
    x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    
    state[x1, y1, z1], state[x2, y2, z2] = state[x2, y2, z2], state[x1, y1, z1]
    
    return state


def genetic_algorithm(population_size, max_iterations, mutation_rate):
    # Initialize the population
    population = initialize_population(population_size)
    
    for iteration in range(max_iterations):
        # Generate a new population
        new_population = []
        while len(new_population) < population_size:
            # Select parents using roulette wheel selection
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)
            print(f"parent1 {parent1.fitness_value} -  {parent1.worst_lines[0][1]}")
            print(f"parent2 {parent2.fitness_value} -  {parent2.worst_lines[0][1]}")
            
            # Apply crossover to produce two children
            child1, child2 = crossover_optimized(parent1, parent2)
            print(f"child {child1.fitness_value} - {child2.fitness_value}")
            
            # Apply mutation to children
            if random.random() < mutation_rate:
                child1.state = mutate(child1.state)
                child1.fitness_value = child1.calculate_fitness()
            if random.random() < mutation_rate:
                child2.state = mutate(child2.state)
                child2.fitness_value = child2.calculate_fitness()
                
            new_population.append(child1)
            new_population.append(child2)
        
        # Update the population for the next iteration
        population = new_population[:population_size]
        
        # Check if goal found alias 315
        best_individual = min(population, key=lambda cube: cube.fitness_value)
        # if isGoalState(best_individual): 
        if best_individual.fitness_value == 315: 
            print(f"Solution found in iteration {iteration}")
            return best_individual
        
        print(f"Iteration {iteration}: Best fitness = {best_individual.fitness_value}\n\n")
    
    print("No perfect solution found within the maximum iterations.")
    return best_individual

best_individual = genetic_algorithm(4, 10, 0.05)