import matplotlib.pyplot as plt

def plot_cube_state(cube, iteration):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f"Iteration {iteration} - Fitness: {cube.fitness_value:.2f}", fontsize=14, fontweight='bold')

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_zlim(0, 5)
    ax.set_box_aspect([1, 1, 1])

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    for z in range(5):
        for y in range(5):
            for x in range(5):
                value = cube.state[z, y, x]

                ax.plot([x, x+1], [y, y], [z, z], color="black", lw=0.5)
                ax.plot([x, x+1], [y+1, y+1], [z, z], color="black", lw=0.5)
                ax.plot([x, x], [y, y+1], [z, z], color="black", lw=0.5)
                ax.plot([x+1, x+1], [y, y+1], [z, z], color="black", lw=0.5)
                
                ax.plot([x, x+1], [y, y], [z+1, z+1], color="black", lw=0.5)
                ax.plot([x, x+1], [y+1, y+1], [z+1, z+1], color="black", lw=0.5)
                ax.plot([x, x], [y, y+1], [z+1, z+1], color="black", lw=0.5)
                ax.plot([x+1, x+1], [y, y+1], [z+1, z+1], color="black", lw=0.5)
                
                ax.plot([x, x], [y, y], [z, z+1], color="black", lw=0.5)
                ax.plot([x+1, x+1], [y, y], [z, z+1], color="black", lw=0.5)
                ax.plot([x, x], [y+1, y+1], [z, z+1], color="black", lw=0.5)
                ax.plot([x+1, x+1], [y+1, y+1], [z, z+1], color="black", lw=0.5)

                ax.text(x + 0.5, y + 0.5, z + 0.5, f"{value}", ha='center', va='center',
                        color='black', fontsize=10, fontweight='bold')

    ax.view_init(elev=20, azim=30)

    plt.show()

def plot_fitness_per_iteration(fitness_value_per_iteration):
    is_random_restart = any(isinstance(value, dict) for value in fitness_value_per_iteration.values())
    plt.figure(figsize=(10, 6))
    
    if is_random_restart:
        for restart, iterations_dict in fitness_value_per_iteration.items():
            iterations = list(iterations_dict.keys())
            fitness_values = list(iterations_dict.values())
            plt.plot(iterations, fitness_values, label=f"Random Restart {restart}", linestyle="--")
    else:
        iterations = list(fitness_value_per_iteration.keys())
        fitness_values = list(fitness_value_per_iteration.values())
        plt.plot(iterations, fitness_values, marker='o',  color='purple', label="Fitness Value")

    plt.title("Fitness Value over Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness Value")
    plt.legend()
    plt.grid(True)
    
    plt.show()
