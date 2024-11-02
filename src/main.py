# main.py
import sys
from genetic_algorithm import genetic_algorithm
from cube import Cube

def print_header():
    print("=" * 50)
    print("Welcome to the 5x5x5 Magic Cube Solver")
    print("=" * 50)
    print("Choose a local search method to solve the magic cube:")
    print("1. Steepest Ascent Hill Climbing")
    print("2. Hill Climbing with Sideways Move")
    print("3. Stochastic Hill Climbing")
    print("4. Simulated Annealing")
    print("5. Genetic Algorithm")
    print("=" * 50)

def main():
    # Print the header
    print("=" * 50)
    print("Welcome to the 5x5x5 Magic Cube Solver")
    print("=" * 50)
    print("Choose a local search method to solve the magic cube:")
    print("1. Steepest Ascent Hill Climbing")
    print("2. Hill Climbing with Sideways Move")
    print("3. Stochastic Hill Climbing")
    print("4. Simulated Annealing")
    print("5. Genetic Algorithm")
    print("=" * 50)

    # Get the user's choice
    try:
        choice = int(input("Enter the number of your choice (1-5): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        sys.exit(1)

    # Execute the chosen algorithm
    if choice == 1:
        print("Steepest Ascent Hill Climbing is under development.")
    elif choice == 2:
        print("Hill Climbing with Sideways Move is under development.")
    elif choice == 3:
        print("Stochastic Hill Climbing is under development.")
    elif choice == 4:
        print("Simulated Annealing is under development.")
    elif choice == 5:
        # Parameters for genetic algorithm
        population_size = 10
        max_generations = 5
        mutation_rate = 0.15

        print("\nStarting Genetic Algorithm...")
        solution = genetic_algorithm(population_size, max_generations, mutation_rate)
        
        # Display the solution
        print("\nSolution found by Genetic Algorithm:")
        solution.display()
        print("Fitness Value:", solution.fitness_value)
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
