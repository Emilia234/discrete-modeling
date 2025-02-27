import numpy as np

WEIGHTS = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
DIRECTIONS = [
    (0, 0), (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (-1, 1), (-1, -1), (1, -1)
]
TAU = 1.0

def compute_concentration(grid):
    return np.sum(grid["f_in"], axis=-1)

def compute_velocity(grid):
    rho = compute_concentration(grid) + 1e-10
    velocity_x = np.sum(grid["f_in"] * np.array([d[0] for d in DIRECTIONS]), axis=-1) / rho
    velocity_y = np.sum(grid["f_in"] * np.array([d[1] for d in DIRECTIONS]), axis=-1) / rho
    grid["velocity_x"], grid["velocity_y"] = velocity_x, velocity_y

def equilibrium_distribution(velocity_x, velocity_y, rho):
    u_squared = velocity_x ** 2 + velocity_y ** 2
    f_eq = np.zeros((velocity_x.shape[0], velocity_x.shape[1], len(DIRECTIONS)))
    for i, (dx, dy) in enumerate(DIRECTIONS):
        ci_dot_u = dx * velocity_x + dy * velocity_y
        f_eq[..., i] = WEIGHTS[i] * rho * (1 + 3 * ci_dot_u + 4.5 * ci_dot_u**2 - 1.5 * u_squared)
    return f_eq

def collision_step(grid):
    compute_velocity(grid)
    rho = compute_concentration(grid)
    grid["f_eq"] = equilibrium_distribution(grid["velocity_x"], grid["velocity_y"], rho)
    grid["f_out"] = grid["f_in"] + (1 / TAU) * (grid["f_eq"] - grid["f_in"])

REVERSE_DIRECTION = {
    0: 0,
    1: 2,
    2: 1,
    3: 4,
    4: 3,
    5: 6,
    6: 5,
    7: 8,
    8: 7
}
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
                        reverse_dir = REVERSE_DIRECTION[i]
                        new_f_in[x, y, reverse_dir] += f_value

    grid["f_in"] = new_f_in




