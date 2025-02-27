import numpy as np

#prawo, dół, lewo, góra
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
NUM_DIRECTIONS = len(DIRECTIONS)

def perform_streaming(grid, obstacles):
    new_grid = np.zeros_like(grid)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            for d, (dx, dy) in enumerate(DIRECTIONS):
                if grid[x, y][d] == 1:
                    nx, ny = x + dx, y + dy

                    if obstacles[nx % grid.shape[0], ny % grid.shape[1]] == 1:
                        opposite_dir = (d + 2) % NUM_DIRECTIONS
                        new_grid[x, y][opposite_dir] = 1
                    else:
                        new_grid[nx % grid.shape[0], ny % grid.shape[1]][d] = 1

    return new_grid

def perform_collision(grid):

    new_grid = np.zeros_like(grid)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            cell_state = grid[x, y]

            if np.array_equal(cell_state, [1, 0, 1, 0]):
                new_grid[x, y] = [0, 1, 0, 1]
            elif np.array_equal(cell_state, [0, 1, 0, 1]):
                new_grid[x, y] = [1, 0, 1, 0]
            else:
                new_grid[x, y] = cell_state

    return new_grid

def update_grid(grid, obstacles):
    grid = perform_streaming(grid, obstacles)
    grid = perform_collision(grid)
    return grid
