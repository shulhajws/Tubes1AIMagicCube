from cube import Cube
from steepest_hill_climb import SteepestHillClimb
from sideways_hill_climb import SidewaysHillClimb
from random_restart_hill_climb import RandomRestartHillClimb
from stochastic_hill_climb import StochasticHillClimb
from simulated_annealing_algorithm import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm
from visualizer import plot_cube_state
from cube_replay import CubeReplayPlayer, isReplayIncluded
import tkinter as tk
import time

def generate_cube():
    print()
    print("Generating Initial Cube State...")
    cube = Cube()
    
    time.sleep(0.6)
    print()
    print("Initial Cube State:")
    cube.display()
    print("Initial Fitness:", cube.fitness_value)
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
        print("3. Exit")

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
                    result, final_iteration = climber.climb(output_file)
                elif ans == "2":
                    climber = SidewaysHillClimb(cube)
                    result, final_iteration = climber.climb(output_file)
                elif ans == "3":
                    climber = RandomRestartHillClimb(cube)
                    result, final_iteration = climber.climb(output_file)
                elif ans == "4":
                    climber = StochasticHillClimb(cube)
                    result, final_iteration = climber.climb(output_file)
                elif ans == "5":
                    algorithm = SimulatedAnnealing(cube)
                    result, final_iteration = algorithm.simulated_annealing_algorithm(0.5, output_file)
                elif ans == "6":
                    print("Genetic Algorithm is not yet implemented.")
                elif ans == "7":
                    break   
                
                
                print()
                print("Final Cube State after Climbing:")
                result.display()
                print("Final Fitness:", result.fitness_value)

                print()
                ans = input("Do you want to see the final cube's 3d representation? (y/n): ")
                if ans.lower() == "y":
                    plot_cube_state(result, final_iteration)
                
                if output_file:
                    ans = input("Do you want to watch the replay of the cube solving process? (y/n): ")
                    if ans.lower() == "y":
                        play_cube_replay(output_file)

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
            print()
            print("Thank you for using Diagonal Magic Cube Solver!")
            return

if __name__ == "__main__":
    main()
