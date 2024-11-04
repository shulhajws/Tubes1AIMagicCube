import tkinter as tk
from tkinter import filedialog
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

class CubeReplayPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Cube Replay Player")

        self.play_pause_button = tk.Button(master, text="Play", command=self.play_pause)
        self.play_pause_button.pack()

        self.progress = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_frame)
        self.progress.pack(fill=tk.X)

        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_label = tk.Label(master, text="Playback Speed:")
        self.speed_label.pack()
        self.speed_scale = tk.Scale(master, from_=0.1, to=3.0, orient=tk.HORIZONTAL, variable=self.speed_var, resolution=0.1)
        self.speed_scale.pack()

        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack()

        self.cube_data = []
        self.current_frame = 0
        self.playing = False
        self.play_event = None

    def load_file(self, file_name=None):
        if not file_name:
            file_path = filedialog.askopenfilename(title="Select Experiment File", filetypes=[("JSON files", "*.json")])
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "../result", file_name)
        
        if not file_path:
            print("No file selected. Returning to main menu.")
            return

        with open(file_path, 'r') as file:
            self.cube_data = json.load(file)
        self.progress.config(to=len(self.cube_data) - 1)
        self.current_frame = 0
        self.update_frame(self.current_frame)
        self.play_pause()

    def play_pause(self):
        self.playing = not self.playing
        self.play_pause_button.config(text="Pause" if self.playing else "Play")
        if self.playing:
            self.play()

    def stop(self):
        self.playing = False
        if self.play_event is not None:
            self.master.after_cancel(self.play_event)
        
        self.master.quit()
        self.master.destroy()

    def play(self):
        if self.playing and self.current_frame < len(self.cube_data):
            self.update_frame(self.current_frame)
            self.current_frame += 1
            self.progress.set(self.current_frame)
            self.play_event = self.master.after(int(1000 / self.speed_var.get()), self.play)
        else:
            self.playing = False
            self.play_pause_button.config(text="Play")

    def update_frame(self, frame):
        self.current_frame = int(self.progress.get())
        state_data = self.cube_data[self.current_frame]
        self.ax.clear()
        plot_cube_state(self.ax, state_data["state"], state_data["iteration"], state_data["fitness_value"])
        self.canvas.draw()

def plot_cube_state(ax, cube_state, iteration, fitness_value):
    ax.set_title(f"Iteration {iteration} - Fitness: {fitness_value:.2f}", fontsize=14, fontweight='bold')
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
                value = cube_state[z][y][x]
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

                ax.text(x + 0.5, y + 0.5, z + 0.5, f"{value}", ha='center', va='center', color='black', fontsize=10, fontweight='bold')

def isReplayIncluded():
    ans_replay = input("Do you want to keep the replay of the cube solving process? (y/n): ")
    if ans_replay.lower() == "y":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        result_dir = os.path.join(base_dir, "../result")

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        while True:
            file_name = input("Enter the output file name (without extension): ")
            file_path = os.path.join(result_dir, f"{file_name}.json")

            if os.path.isfile(file_path):
                print(f"The file '{file_name}.json' already exists in the 'result/' directory.")
                ans = input("Do you want to overwrite the file? (y/n): ")
                if ans.lower() == "y":
                    open(file_path, 'w').close()
                    print(f"The file '{file_name}.json' will be overwritten.")
                    return file_name+".json"
                else:
                    print("Please enter a new file name.")
            else:
                print(f"The file will be saved as '{file_name}.json' in the 'result/' directory.")
                return file_name+".json"
    else:
        return None