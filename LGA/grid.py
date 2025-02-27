import numpy as np

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Prawo, Dół, Lewo, Góra

def create_grid(grid_size, barrier_coords):
    grid = np.zeros(grid_size + (4,), dtype=int)
    obstacles_grid = np.zeros(grid_size, dtype=int)

    for x, y in barrier_coords:
        if obstacles_grid[x, y] == 0:
            obstacles_grid[x, y] = 1

    return grid, obstacles_grid

def initialize_particles(grid, density, barrier_col=25):
    for x in range(grid.shape[0]):
        for y in range(barrier_col):
            if np.random.random() < density:
                direction = np.random.choice(len(DIRECTIONS))
                grid[x, y][direction] = 1
    return grid

