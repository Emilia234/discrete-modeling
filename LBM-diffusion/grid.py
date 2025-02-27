import numpy as np

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def create_grid(grid_size, barrier_coords):
    grid = {
        "f_in": np.zeros(grid_size + (4,), dtype=float),
        "f_eq": np.zeros(grid_size + (4,), dtype=float),
        "f_out": np.zeros(grid_size + (4,), dtype=float),
        "concentration": np.zeros(grid_size, dtype=float)
    }
    obstacles_grid = np.zeros(grid_size, dtype=int)

    for x, y in barrier_coords:
        obstacles_grid[x, y] = 1

    return grid, obstacles_grid

def initialize_particles(grid, density_left, density_right, barrier_col=25, obstacles=None):
    grid_height, grid_width = grid["f_in"].shape[:2]
    for x in range(grid_height):
        for y in range(grid_width):
            if obstacles[x, y] == 0:

                if y < barrier_col:
                    grid["f_in"][x, y] = density_left/4
                    grid["concentration"][x, y] = density_left
                elif y >= barrier_col:
                    grid["f_in"][x, y] = density_right/4
                    grid["concentration"][x, y] = density_right
            else:
                grid["f_in"][x, y, :] = 0.0
                grid["concentration"][x, y] = 0.0









