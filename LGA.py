from grid import create_grid, initialize_particles
from dynamics import update_grid
from visualization import run_visualization, initialize, draw_grid

import pygame

GRID_SIZE = (50, 100)
DENSITY = 0.8

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


# def show_initial_state(screen, grid, obstacles):
#     draw_grid(screen, grid, obstacles)
#
#     waiting = True
#     while waiting:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             elif event.type == pygame.KEYDOWN:  # Kontynuacja po naciśnięciu klawisza
#                 waiting = False


def main():
    grid, obstacles = create_grid(GRID_SIZE, ALL_BARRIERS)
    initialize_particles(grid, DENSITY, barrier_col=25)

   #  screen, clock = initialize(GRID_SIZE)
   #  show_initial_state(screen, grid, obstacles)
    run_visualization(grid, obstacles, update_grid, steps=1000)
if __name__ == "__main__":
    main()
