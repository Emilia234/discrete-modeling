import pygame

CELL_SIZE = 10
FPS = 30

def initialize(grid_size):
    pygame.init()
    width, height = grid_size[1] * CELL_SIZE, grid_size[0] * CELL_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Symulacja LBM")
    clock = pygame.time.Clock()
    return screen, clock

def draw_grid(screen, grid, obstacles):
    screen.fill((0, 0, 0))

    for x in range(grid["concentration"].shape[0]):
        for y in range(grid["concentration"].shape[1]):
            concentration_value = grid["concentration"][x, y]
            color_intensity = min(255, max(0, int(concentration_value * 255)))

            color = (color_intensity, color_intensity, color_intensity)

            if concentration_value > 0:
                pygame.draw.rect(
                    screen, color,
                    (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
            if obstacles[x, y] == 1:
                pygame.draw.rect(
                    screen, (255, 0, 0),
                    (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    pygame.display.flip()

def run_visualization(grid, obstacles, collision_step, streaming_step, steps=500):
    grid_size = grid["f_in"].shape[:2]
    screen, clock = initialize(grid_size)

    running = True
    step = 0

    while running and step < steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        collision_step(grid)
        streaming_step(grid, obstacles)
        draw_grid(screen, grid, obstacles)

        clock.tick(FPS)
        step += 1

    pygame.quit()
