from cube import Cube
from steepest_hill_climb import SteepestHillClimb
from sideways_hill_climb import SidewaysHillClimb
from random_restart_hill_climb import RandomRestartHillClimb
from stochastic_hill_climb import StochasticHillClimb
from simulated_annealing_algorithm import SimulatedAnnealing
from genetic_algorithm import genetic_algorithm

from visualizer import plot_cube_state, plot_objective_function
from cube_replay import CubeReplayPlayer, isReplayIncluded
import tkinter as tk
import time
import os

def generate_cube():
    print()
    print("Generating Initial Cube State...")
    cube = Cube()
    
    time.sleep(0.6)
    print()
    print("Initial Cube State:")
    cube.display()
    print(f"Initial Fitness: {cube.fitness_value:.2f}")
    print()

    ans = input("Do you want to see the cube's 3d representation? (y/n): ")
    if ans.lower() == "y":
        plot_cube_state(cube, 0)
    
    return cube

def play_cube_replay(output_file=None):
    root = tk.Tk()
    player = CubeReplayPlayer(root)
    player.load_file(output_file)
    root.protocol("WM_DELETE_WINDOW", player.stop)
    root.mainloop()

def main():
    print("Welcome to Diagonal Magic Cube Solver!")
    time.sleep(0.5)
    print("This program is created by Group 30 of IF3170 - Artificial Intelligence 2024/2025.")
    time.sleep(0.5)
    print("13522050 - Kayla Namira Mariadi")
    time.sleep(0.5)
    print("13522060 - Andhita Naura Hariyanto")
    time.sleep(0.5)
    print("13522062 - Salsabiila")
    time.sleep(0.5)
    print("13522087 - Shulha")

    while True:
        print()
        print("Main Menu: ")
        print("1. Solve a cube")
        print("2. Play a cube replay")
        print("3. See a cube's objective function value over iterations")
        print("4. Exit")

        while True:
            ans = input("Choose the action you want to do: ")
            if ans in ["1", "2", "3"]:
                break
            print("Invalid input. Please try again.")
            print()

        if ans == "1":
            cube = generate_cube()
            
            while True:
                print()
                print("Local Search Algorithms:")
                print("1. Steepest Hill Climbing")
                print("2. Hill Climbing with Sideways Move")
                print("3. Random Restart Hill Climbing")
                print("4. Stochastic Hill Climbing")
                print("5. Simulated Annealing")
                print("6. Genetic Algorithm")
                print("7. Back to Main Menu")

                while True:
                    ans = input("Choose the algorithm you want to use: ")
                    if ans in ["1", "2", "3", "4", "5", "6", "7"]:
                        break
                    print("Invalid input. Please try again.")
                    print()
                
                print()
                output_file = isReplayIncluded()

                if ans == "1":
                    climber = SteepestHillClimb(cube)

                    max_iteration = int(input("Input the maximum iteration (default 1000): "))
                    print()

                    if not max_iteration:
                        max_iteration = 1000
                    
                    result, final_iteration, final_time = climber.climb(output_file, max_iteration)

                elif ans == "2":
                    climber = SidewaysHillClimb(cube)

                    max_iteration = int(input("Input the maximum iteration (default 1000): "))
                    print()

                    if not max_iteration:
                        max_iteration = 1000
                    
                    result, final_iteration, final_time = climber.climb(output_file, max_iteration)

                elif ans == "3":
                    climber = RandomRestartHillClimb(cube)

                    max_restart = int(input("Input the maximum restart (default 20): "))
                    max_iteration = int(input("Input the maximum iteration (default 1000): "))
                    print()

                    if not max_restart:
                        max_restart = 20
                    if not max_iteration:
                        max_iteration = 1000

                    result, final_iteration, iterations_per_restart, final_time = climber.climb(output_file, max_restart, max_iteration)
                    for restart in iterations_per_restart:
                        print(f"Restart: {restart[0]} - Jumlah Iterasi: {restart[1]}\n")

                elif ans == "4":
                    climber = StochasticHillClimb(cube)

                    max_iteration = int(input("Input the maximum iteration (default 1000): "))
                    print()

                    if not max_iteration:
                        max_iteration = 1000

                    result, final_iteration, final_time = climber.climb(output_file, max_iteration)

                elif ans == "5":
                    algorithm = SimulatedAnnealing(cube)

                    threshold = float(input("Input the threshold (default 0.5): "))
                    print()

                    if not threshold:
                        threshold = 0.5
                    
                    result, final_iteration, final_time = algorithm.simulated_annealing_algorithm(threshold, output_file)

                elif ans == "6":
                    population_size = int(input("Input the population size: "))
                    max_iterations = int(input("Input the maximum iteration: "))
                    mutation_rate = float(input("Input the mutation rate (Between 0 and 1): "))
                    print()
                    
                    result, final_iteration, final_time = genetic_algorithm(population_size, max_iterations, mutation_rate, output_file)

                elif ans == "7":
                    break   
                
                print("\n\n")
                print(f"Final cube state is reached after {final_iteration} iterations in {final_time:.2f} seconds.")
                print()
                print("Final cube state after climbing:")
                result.display()
                print(f"Final Fitness: {result.fitness_value:.2f}")

                print()
                ans = input("Do you want to see the final cube's 3d representation? (y/n): ")
                if ans.lower() == "y":
                    plot_cube_state(result, final_iteration)
                
                print()
                ans = input("Do you want to see the objective function value over iterations? (y/n): ")
                if ans.lower() == "y":
                    plot_objective_function(output_file)
                
                if output_file != "temp-68943268950973503917903-347909730149437079043.json":
                    ans = input("Do you want to watch the replay of the cube solving process? (y/n): ")
                    if ans.lower() == "y":
                        play_cube_replay(output_file)
                else:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    result_dir = os.path.join(base_dir, "../result")
                    file_dir = os.path.join(result_dir, output_file)
                    os.remove(file_dir)

                print()
                print("Cube Menu:")
                print("1. Choose Local Search Algorithm")
                print("2. Generate New Cube")
                print("3. Back to Main Menu")
                print("4. Exit")

                while True:
                    ans = input("Choose the action you want to do: ")
                    if ans in ["1", "2", "3", "4"]:
                        break
                    print("Invalid input. Please try again.")
                    print()

                if ans == "1":
                    continue
                elif ans == "2":
                    cube = generate_cube()
                elif ans == "3":
                    break
                elif ans == "4":
                    print()
                    print("Thank you for using Diagonal Magic Cube Solver!")
                    return

        elif ans == "2":
            play_cube_replay()
            continue

        elif ans == "3":
            output_file = input("Enter the output file name (without extension): ")
            plot_objective_function(output_file)
            continue

        elif ans == "4":
            print()
            print("Thank you for using Diagonal Magic Cube Solver!")
            return

if __name__ == "__main__":
    main()
