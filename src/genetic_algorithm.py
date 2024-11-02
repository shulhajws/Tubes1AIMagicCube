import random
from cube import Cube,np

def roulette_wheel_selection(population):
    """Select a parent from the population using roulette wheel selection based on fitness."""
    total_fitness = sum(cube.fitness_value for cube in population)
    relative_fitness = [cube.fitness_value / total_fitness for cube in population]
    cumulative_probabilities = np.cumsum(relative_fitness)

    rand = random.random()
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if rand <= cumulative_probability:
            return population[i]
    return population[-1]

def initialize_population(population_size):
    """Initialize a population of Cube objects with random states."""
    return [Cube() for _ in range(population_size)]

def crossover(parent1, parent2):
    """partially mapped crossover """
    child1_state = np.copy(parent1.state)
    child2_state = np.copy(parent2.state)
    
    # Choose a random layer 
    layer = random.randint(0, 4)
    print(f"Performing crossover on z-layer {layer}")

    # Extract the slices from the chosen layer
    slice1 = parent1.state[:, :, layer]
    slice2 = parent2.state[:, :, layer]
    
    # Choose crossover points within the layer
    row_start, row_end = sorted(random.sample(range(5), 2))
    col_start, col_end = sorted(random.sample(range(5), 2))
    
    # Copy the crossover area from parent slices to child slices
    child1_slice = np.copy(slice1)
    child2_slice = np.copy(slice2)
    
    # PMX mappings for the area
    mapping1 = {}
    mapping2 = {}
    
    # Create mappings for values within the crossover region
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            val1 = slice1[i, j]
            val2 = slice2[i, j]
            child1_slice[i, j] = val2
            child2_slice[i, j] = val1
            mapping1[val2] = val1   
            mapping2[val1] = val2  
    
    # Resolve conflicts in child1_slice
    for h in range (5):
        for i in range(5):
            for j in range(5):
                if not (h==4 and row_start <= i <= row_end and col_start <= j <= col_end):
                    if parent1.state[h,i,j] in mapping1:
                        parent1.state[h,i,j] = mapping1[parent1.state[h,i,j]]
                    # original_value = child1_slice[i, j]
                    # while original_value in mapping1:
                    #     original_value = mapping1[original_value]
                    # child1_slice[i, j] = original_value

    # Resolve conflicts in child2_slice
    for h in range (5):
        for i in range(5):
            for j in range(5):
                if not (h==4 and row_start <= i <= row_end and col_start <= j <= col_end):
                    if parent2.state[h,i,j] in mapping2:
                        parent2.state[h,i,j] = mapping2[parent2.state[h,i,j]]
                    # original_value = child2_slice[i, j]
                    # while original_value in mapping2:
                    #     original_value = mapping2[original_value]
                    # child2_slice[i, j] = original_value

    # Place the modified slices back into the children states
    child1_state[:, :, layer] = child1_slice
    child2_state[:, :, layer] = child2_slice
    
    # Return new Cube objects as children
    return Cube(child1_state), Cube(child2_state)

def mutate(state):
    """Mutate a cube state by randomly swapping two elements."""
    x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    
    state[x1, y1, z1], state[x2, y2, z2] = state[x2, y2, z2], state[x1, y1, z1]
    
    return state


def genetic_algorithm(population_size, max_generations, mutation_rate):
    """Genetic Algorithm general function."""
    # Initialize the population
    population = initialize_population(population_size)
    
    for generation in range(max_generations):
        best_individual = min(population, key=lambda cube: cube.fitness_value)
        # if isGoalState(best_individual): 
        #     print(f"Solution found in generation {generation}")
        #     return best_individual
        
        # Generate a new population
        new_population = []
        while len(new_population) < population_size:
            # Select parents using roulette wheel selection
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)
            
            # Apply crossover to produce two children
            child1, child2 = crossover(parent1, parent2)
            
            # Apply mutation to children
            if random.random() < mutation_rate:
                child1.state = mutate(child1.state)
                child1.fitness_value = child1.calculate_fitness()
            if random.random() < mutation_rate:
                child2.state = mutate(child2.state)
                child2.fitness_value = child2.calculate_fitness()
                
            new_population.append(child1)
            new_population.append(child2)
        
        # Update the population for the next generation
        population = new_population[:population_size]
        
        print(f"Generation {generation}: Best fitness = {best_individual.fitness_value}")
    
    print("No perfect solution found within the maximum generations.")
    return best_individual