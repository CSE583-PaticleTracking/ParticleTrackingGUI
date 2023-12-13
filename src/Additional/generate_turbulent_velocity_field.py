"""
Module to generate a turbulent velocity field using Perlin noise. 
The turbulent velocity field is generated as a list
of frames, where each frame is a 3D array of shape (grid_size, grid_size, 2), 
where the last dimension contains the u and v components of the velocity 
field. The frames can be saved to CSV files using the save_frames_to_csv function.
The frames can be plotted using the plot_frame function. The turbulent velocity 
field can be generated using the generate_turbulent_velocity_field 
function.
Components:
    * generate_turbulent_velocity_field - generates a turbulent velocity field.
    * save_frames_to_csv - saves the frames to CSV files.
    * plot_frame - plots the velocity field of a frame.
Examples:
    # Generate a turbulent velocity field
    turbulent_frames = generate_turbulent_velocity_field(grid_size, num_frames)
    # Save the frames to CSV files
    save_frames_to_csv(turbulent_frames)
    # Plot the velocity field of a frame
    plot_frame(frame)
    """
import os
import numpy as np
import noise
import csv
import matplotlib.pyplot as plt

def generate_turbulent_velocity_field(grid_size, num_frames, amplitude = 10000, persistence=0.5, lacunarity=2.0, scale=500.0):
    frames = []

    base = np.linspace(10,20,num_frames)
    for _ in range(num_frames):
        # Generate 2D Perlin noise
        # base = np.random.randint(0, 1000)
        world = np.empty((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                world[i][j] = noise.pnoise2(
                    (i + base[_]) / scale,
                    (j + base[_]) / scale,
                    octaves=6,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=0,
                )

        # Calculate the gradient
        dx, dy = np.gradient(world)

        # Calculate the velocity field
        u = amplitude * (-dy)
        v = amplitude * dx

        # Append the frame to the list
        frames.append(np.stack((u, v), axis=-1))

    return frames

def save_frames_to_csv(frames, folder_path="turbulent_frames"):
    """
    Save the frames to CSV files. Each CSV file contains the x and y coordinates of the grid points, and the u and v
    components of the velocity field at each grid point.
    Inputs:
        frames (list): List of frames to be saved.
        folder_path (str): Path to the folder where the CSV files will be saved.
    Outputs:
        None
    Examples:
        save_frames_to_csv(turbulent_frames)
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, frame in enumerate(frames):
        csv_file_path = f"{folder_path}/frame_{i}.csv"
        header = ["x", "y", "u", "v"]

        data = [(x, y, u, v) for x, row_x in enumerate(frame) for y, (u, v) in enumerate(row_x)]

        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(data)

        print(f"Frame {i} saved to {csv_file_path}")

def plot_frame(frame, title="Turbulent Velocity Field"):
    """
    Plot the velocity field of a frame. The frame is a 3D array of shape (grid_size, grid_size, 2), where the last
    dimension contains the u and v components of the velocity field.
    Inputs:
        frame (numpy.ndarray): 3D array containing the velocity field.
        title (str): Title of the plot.
    Outputs:
        None
    Examples:
        plot_frame(frame)
    """
    u = frame[:, :, 0]
    v = frame[:, :, 1]

    plt.figure(figsize=(8, 8))
    plt.quiver(u, v, scale=20, scale_units='xy', angles='xy', cmap='viridis')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

if __name__ == "__main__":
    grid_size = 100
    num_frames = 25

    turbulent_frames = generate_turbulent_velocity_field(grid_size, num_frames)
    save_frames_to_csv(turbulent_frames)

    # for i, frame in enumerate(turbulent_frames):
    #     plot_frame(frame, title=f"Turbulent Velocity Field - Frame {i}")
