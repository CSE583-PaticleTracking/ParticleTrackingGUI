import os
import numpy as np
import noise
import csv
import matplotlib.pyplot as plt

def generate_turbulent_velocity_field(grid_size, num_frames, amplitude = 10000, persistence=0.5, lacunarity=2.0, scale=500.0):
    frames = []
    print(frames)
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
        print(frames)
        # Calculate the gradient
        dx, dy = np.gradient(world)

        # Calculate the velocity field
        u = amplitude * (-dy)
        v = amplitude * dx

        # Append the frame to the list
        frames.append(np.stack((u, v), axis=-1))

    return frames

def save_frames_to_csv(frames, folder_path="turbulent_frames"):
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
    u = frame[:, :, 0]
    v = frame[:, :, 1]

    plt.figure(figsize=(8, 8))
    plt.quiver(u, v, scale=20, scale_units='xy', angles='xy', cmap='viridis')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

if __name__ == "__main__":
    grid_size = 5
    num_frames = 5

    turbulent_frames = generate_turbulent_velocity_field(grid_size, num_frames)
    save_frames_to_csv(turbulent_frames)

    for i, frame in enumerate(turbulent_frames):
        plot_frame(frame, title=f"Turbulent Velocity Field - Frame {i}")
