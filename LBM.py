from grid import create_grid, initialize_particles
from dynamics import collision_step, streaming_step
from visualization import run_visualization

GRID_SIZE = (50, 100)
DENSITY_LEFT = 1.0
DENSITY_RIGHT = 0.0

grid_height = GRID_SIZE[0]
gap_start = grid_height // 2 - 3
gap_end = grid_height // 2 + 3

BARRIER_COORDS = [
    (x, 25) for x in range(GRID_SIZE[0]) if not (gap_start <= x < gap_end)
]
BORDER_COORDS = (
        [(0, y) for y in range(GRID_SIZE[1])] +
        [(GRID_SIZE[0] - 1, y) for y in range(GRID_SIZE[1])] +
        [(x, 0) for x in range(GRID_SIZE[0])] +
        [(x, GRID_SIZE[1] - 1) for x in range(GRID_SIZE[0])]
)
ALL_BARRIERS = BARRIER_COORDS + BORDER_COORDS


def main():
    grid, obstacles = create_grid(GRID_SIZE, ALL_BARRIERS)
    initialize_particles(grid, DENSITY_LEFT, DENSITY_RIGHT, barrier_col=25, obstacles=obstacles)
    run_visualization(grid, obstacles, collision_step, streaming_step, steps=10000000000000000)

if __name__ == "__main__":
    main()
