import numpy as np
WEIGHTS = [1/4, 1/4, 1/4, 1/4]
TAU = 1
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def compute_concentration(grid):
    return np.sum(grid["f_in"], axis=-1)

def equilibrium_distribution(concentration):
    f_eq = np.zeros(concentration.shape + (4,))
    for i, (dx, dy) in enumerate(DIRECTIONS):
        f_eq[..., i] = WEIGHTS[i] * concentration
    return f_eq

def collision_step(grid):
    concentration = compute_concentration(grid)
    grid["concentration"] = concentration

    grid["f_eq"] = equilibrium_distribution(concentration)

    grid["f_out"] = grid["f_in"] + (1 / TAU) * (grid["f_eq"] - grid["f_in"])

def streaming_step(grid, obstacles):
    new_f_in = np.zeros_like(grid["f_in"])
    rows, cols = grid["f_in"].shape[:2]

    for i, (dx, dy) in enumerate(DIRECTIONS):
        for x in range(1, rows - 1):
            for y in range(1, cols - 1):
                f_value = grid["f_out"][x, y, i]

                if f_value > 0:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and obstacles[nx, ny] == 0:
                        new_f_in[nx, ny, i] += f_value
                    else:
                        reverse_dir = (i + 2) % 4
                        new_f_in[x, y, reverse_dir] += f_value
    grid["f_in"] = new_f_in














