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

def crossover(parent1, parent2):
    layer=[0,1,2,3,4]
    """partially mapped crossover """
    child1 = np.copy(parent1.state)
    child2 = np.copy(parent2.state)

    # PMX mappings for the area
    mapping1 = {}
    mapping2 = {}

    # Choose crossover points within the layer
    # row_start, row_end = sorted(random.sample(range(5), 2))
    # col_start, col_end = sorted(random.sample(range(5), 2))
    row_start, row_end = 0,4
    col_start, col_end = 0,4
    
    # Create mappings and swap values within the crossover region
    for i in layer:
        for j in range(row_start, row_end + 1):
            for k in range(col_start, col_end + 1):
                val1 = parent1.state[i, j, k]
                val2 = parent2.state[i, j, k]
                
                # if val1 != val2:
                    # Swap values in the crossover region
                child1[i, j, k] = val2
                child2[i, j, k] = val1
                
                # Create mappings for conflict resolution
                mapping1[val2] = val1
                mapping2[val1] = val2 

    # print("mapping 2")
    # print(mapping2)
    
    # # Resolve conflicts in child
    for i in range(5):
        for j in range(5):
            for k in range(5):
                # print(i in layer)
                if not ((i in layer) and (row_start <= j <= row_end) and (col_start <= k <= col_end)):
                    original_value_child1 = child1[i, j, k]
                    while original_value_child1 in mapping1:
                        original_value_child1 = mapping1[original_value_child1]
                    child1[i, j, k] = original_value_child1

                    original_value_child2 = child2[i, j, k]
                    while original_value_child2 in mapping2:
                        original_value_child2 = mapping2[original_value_child2]
                    child2[i, j, k] = original_value_child2
                
    # Return new Cube objects as children
    return Cube(child1), Cube(child2)

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
        # # Check if goal found alias 315
        # best_individual = max(population, key=lambda cube: cube.fitness_value)
        # # if isGoalState(best_individual): 
        # if best_individual.fitness_value == 315: 
        #     print(f"Solution found in iteration {iteration}")
        #     return best_individual
        
        # Generate a new population
        new_population = []
        while len(new_population) < population_size:
            # Select parents using roulette wheel selection
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)

            print("parents")
            parent1.display()
            parent2.display()
            
            # Apply crossover to produce two children
            child1, child2 = crossover(parent1, parent2)
            print("children")
            child1.display()
            child2.display()
            
            # Apply mutation to children
            # if random.random() < mutation_rate:
            #     child1.state = mutate(child1.state)
            #     child1.fitness_value = child1.calculate_fitness()
            # if random.random() < mutation_rate:
            #     child2.state = mutate(child2.state)
            #     child2.fitness_value = child2.calculate_fitness()
                
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
        
        print(f"Iteration {iteration}: Best fitness = {best_individual.fitness_value}")
    
    print("No perfect solution found within the maximum iterations.")
    return best_individual

best_individual = genetic_algorithm(8, 10, 0.05)