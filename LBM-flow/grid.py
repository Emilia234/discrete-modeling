import numpy as np

WEIGHTS = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
DIRECTIONS = [
    (0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (-1, 1), (-1, -1), (1, -1)
]
def create_grid(grid_size, barrier_coords):
    grid = {
        "f_in": np.zeros(grid_size + (9,), dtype=float),
        "f_eq": np.zeros(grid_size + (9,), dtype=float),
        "f_out": np.zeros(grid_size + (9,), dtype=float),
        "concentration": np.zeros(grid_size, dtype=float),
        "velocity_x": np.zeros(grid_size, dtype=float),
        "velocity_y": np.zeros(grid_size, dtype=float)
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
                    rho = density_left
                    u_x, u_y = 0.0, 0.0
                else:
                    rho = density_right
                    u_x, u_y = 0.0, 0.0

                u_sq = u_x**2 + u_y**2
                for i, (dx, dy) in enumerate(DIRECTIONS):
                    ci_dot_u = dx * u_x + dy * u_y
                    grid["f_in"][x, y, i] = WEIGHTS[i] * rho * (
                        1 + 3 * ci_dot_u + 4.5 * ci_dot_u**2 - 1.5 * u_sq
                    )

                grid["concentration"][x, y] = rho
            else:
                grid["f_in"][x, y, :] = 0.0
                grid["concentration"][x, y] = 0.0











