import pygame
import numpy as np
from dynamics import compute_concentration

CELL_SIZE = 5
FPS = 30

def initialize(width, height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("LBM Visualization")
    return screen

def velocity_to_color(value, max_value):
    normalized = np.clip(value / max_value, -1.0, 1.0)
    if normalized > 0:
        r = int(8000 * normalized)
        r = min(r, 255)
        return r, 0, 0
    else:
        b = int(8000 * -normalized)
        b = min(b, 255)
        return 0, 0, b


def draw_grid(screen, grid, obstacles_grid, max_speed, section="main"):
    grid_width = grid["velocity_x"].shape[1]
    grid_height = grid["velocity_x"].shape[0]

    if section == "main":
        offset_x = 0
    elif section == "velocity_x":
        offset_x = grid_width * CELL_SIZE
    elif section == "velocity_y":
        offset_x = 2 * grid_width * CELL_SIZE

    for x in range(grid_height):
        for y in range(grid_width):
            if obstacles_grid[x, y] == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (y * CELL_SIZE + offset_x, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
            else:
                if section == "main":
                    color_x = velocity_to_color(grid["velocity_x"][x, y], max_speed)
                    color_y = velocity_to_color(grid["velocity_y"][x, y], max_speed)

                    combined_color = (
                        min(255, color_x[0] + color_y[0]),
                        min(255, color_x[1] + color_y[1]),
                        min(255, color_x[2] + color_y[2])
                    )
                    color = combined_color
                elif section == "velocity_x":
                    color = velocity_to_color(grid["velocity_x"][x, y], max_speed)
                elif section == "velocity_y":
                    color = velocity_to_color(grid["velocity_y"][x, y], max_speed)

                pygame.draw.rect(
                    screen,
                    color,
                    (y * CELL_SIZE + offset_x, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    pygame.display.flip()

def run_visualization(grid, obstacles, collision_step, streaming_step, steps=500, tolerance=1e-6):
    grid_size = grid["f_in"].shape[:2]

    max_speed = max(np.max(np.abs(grid["velocity_x"])), np.max(np.abs(grid["velocity_y"]))) or 1.0
    screen_width = grid_size[1] * CELL_SIZE * 3
    screen_height = grid_size[0] * CELL_SIZE

    screen = initialize(screen_width, screen_height)
    clock = pygame.time.Clock()
    running = True
    step = 0

    prev_concentration = compute_concentration(grid)
    prev_velocity_x = grid["velocity_x"].copy()
    prev_velocity_y = grid["velocity_y"].copy()

    while running and step < steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        collision_step(grid)
        streaming_step(grid, obstacles)

        draw_grid(screen, grid, obstacles, max_speed, section="main")
        draw_grid(screen, grid, obstacles, max_speed, section="velocity_x")
        draw_grid(screen, grid, obstacles, max_speed, section="velocity_y")

        current_concentration = compute_concentration(grid)
        diff_concentration = np.max(np.abs(current_concentration - prev_concentration))
        diff_velocity_x = np.max(np.abs(grid["velocity_x"] - prev_velocity_x))
        diff_velocity_y = np.max(np.abs(grid["velocity_y"] - prev_velocity_y))

        print(f"Step: {step}, ΔConcentration: {diff_concentration}, ΔVelocity_X: {diff_velocity_x}, ΔVelocity_Y: {diff_velocity_y}")

        prev_concentration = current_concentration.copy()
        prev_velocity_x = grid["velocity_x"].copy()
        prev_velocity_y = grid["velocity_y"].copy()

        if diff_concentration < tolerance and diff_velocity_x < tolerance and diff_velocity_y < tolerance:
            print(f"Stan ustalony osiągnięty na kroku {step}.")
            running = False

        clock.tick(FPS)
        step += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return



