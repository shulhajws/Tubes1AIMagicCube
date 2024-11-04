import random
import json
import time
import sys
from cube import Cube,np

def roulette_wheel_selection(population):
    """Select a parent from the population using roulette wheel selection based on fitness."""
    total_fitness = sum(cube.fitness_value for cube in population)
    relative_fitness = [round(cube.fitness_value * 100 / total_fitness, 2) for cube in population]
    cumulative_probabilities = np.cumsum(relative_fitness)

    rand = random.random() * 100
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if rand <= cumulative_probability:
            return population[i]
    return population[-1]

def initialize_population(population_size):
    """Initialize a population of Cube objects with random states."""
    return [Cube() for _ in range(population_size)]

def resolve_mapping_conflicts(child, mapping, crossover_indices):
    """Resolve duplicate values in the child using the mapping."""
    visited = set()

    for index in np.ndindex(child.shape):
        if index in crossover_indices:
            continue  

        value = child[index]
        while value in mapping and value not in visited:
            visited.add(value)
            value = mapping[value]

            if value in visited:
                break  

        child[index] = value

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
    for crossover_idx in range(1):
        # Replace in child1 using parent2's best line
        worst_line_indices_parent1 = parent1.worst_lines[crossover_idx][1]
        best_line_indices_parent2 = parent2.best_lines[crossover_idx][1]

        if worst_line_indices_parent1[2] == -1:  # worst line is a row
            for k in range(5):
                ori_val = child1[worst_line_indices_parent1[0], worst_line_indices_parent1[1], k]
                child1[worst_line_indices_parent1[0], worst_line_indices_parent1[1], k] = parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]
                crossover_index_parent1.append((worst_line_indices_parent1[0], worst_line_indices_parent1[1], k))
                if (ori_val != parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]):
                    mapping1[ori_val] = parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]
                    mapping2[parent2.state[best_line_indices_parent2[0], best_line_indices_parent2[1], k]] = ori_val

        elif worst_line_indices_parent1[1] == -1:  # worst line is a column
            for j in range(5):
                ori_val = child1[worst_line_indices_parent1[0], j, worst_line_indices_parent1[2]]
                child1[worst_line_indices_parent1[0], j, worst_line_indices_parent1[2]] = parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]
                crossover_index_parent1.append((worst_line_indices_parent1[0], j, worst_line_indices_parent1[2]))
                if (ori_val != parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]):
                    mapping1[ori_val] = parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]
                    mapping2[parent2.state[best_line_indices_parent2[0], j, best_line_indices_parent2[2]]] = ori_val

        elif worst_line_indices_parent1[0] == -1:  # Worst line is a pillar
            for i in range(5):
                ori_val = child1[i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]]
                child1[i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]] = parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]
                crossover_index_parent1.append((i, worst_line_indices_parent1[1], worst_line_indices_parent1[2]))
                if (ori_val != parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]):
                    mapping1[ori_val] = parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]
                    mapping2[parent2.state[i, best_line_indices_parent2[1], best_line_indices_parent2[2]]] = ori_val
                    
        if best_line_indices_parent2[2] == -1:  # Best line is a row
            for l in range(5):
                ori_val = child2[best_line_indices_parent2[0], best_line_indices_parent2[1], l]
                child2[best_line_indices_parent2[0], best_line_indices_parent2[1], l] =  parent1.state[worst_line_indices_parent1[0], worst_line_indices_parent1[1], l]
                crossover_index_parent2.append((best_line_indices_parent2[0], best_line_indices_parent2[1], l))
                    

        elif best_line_indices_parent2[1] == -1:  # Best line is a column
            for m in range(5):
                ori_val = child2[best_line_indices_parent2[0], m, best_line_indices_parent2[2]]
                child2[best_line_indices_parent2[0], m, best_line_indices_parent2[2]] = parent1.state[worst_line_indices_parent1[0], m, worst_line_indices_parent1[2]]
                crossover_index_parent2.append((best_line_indices_parent2[0], m, best_line_indices_parent2[2]))

        elif best_line_indices_parent2[0] == -1:  # Best line is a pillar
            for n in range(5):
                ori_val = child2[n, best_line_indices_parent2[1], best_line_indices_parent2[2]] 
                child2[n, best_line_indices_parent2[1], best_line_indices_parent2[2]] = parent1.state[n, worst_line_indices_parent1[1], worst_line_indices_parent1[2]]
                crossover_index_parent2.append((n, best_line_indices_parent2[1], best_line_indices_parent2[2]))
                
    resolve_mapping_conflicts(child1, mapping2, set(crossover_index_parent1))
    resolve_mapping_conflicts(child2, mapping1, set(crossover_index_parent2))

    # Return new Cube objects as children
    return Cube(child1), Cube(child2)

def mutate(state):
    """Mutate a cube state by randomly swapping two elements."""
    x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    
    state[x1, y1, z1], state[x2, y2, z2] = state[x2, y2, z2], state[x1, y1, z1]
    
    return state


def genetic_algorithm(population_size, max_iterations, mutation_rate, output_file=None):
    # Initialize the population
    if output_file:
        history = []

    sys.stdout.write("Loading...\n")
    sys.stdout.flush()

    start_time = time.time()

    population = initialize_population(population_size)
    
    for iteration in range(max_iterations):
        # Generate a new population
        new_population = []
        while len(new_population) < population_size:
            # Select parents using roulette wheel selection
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)
            
            # Apply crossover to produce two children
            child1, child2 = crossover_optimized(parent1, parent2)
            
            # Apply mutation to children
            if random.random() < mutation_rate:
                child1.state = mutate(child1.state)
                child1.fitness_value, _, _ = child1.calculate_fitness()
            if random.random() < mutation_rate:
                child2.state = mutate(child2.state)
                child2.fitness_value, _, _ = child2.calculate_fitness()
                
            new_population.append(child1)
            new_population.append(child2)
           
        # Select the best individuals from the parent and child population
        combined_population = population + new_population
        combined_population.sort(key=lambda cube: cube.fitness_value)
        population = combined_population[:population_size]  
        
        best_individual = population[0]

        if output_file:
            history.append({
                "iteration": iteration + 1,
                "state": [[row.tolist() for row in layer] for layer in best_individual.state],
                "fitness_value": int(best_individual.fitness_value)
            })

            with open("result/"+output_file, "w") as f:
                    json.dump(history, f, indent=4)

        # if isGoalState(best_individual): 
        if best_individual.fitness_value == 0: 
            break

        if iteration % 10 == 0:
                sys.stdout.write("\rCurrent iteration: {}".format(iteration))
                sys.stdout.flush()
                time.sleep(0.1)

    finish_time = time.time()
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.write("\033[F" + " " * 50 + "\r")

    return best_individual, iteration, (finish_time - start_time)