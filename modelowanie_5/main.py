import pygame
import numpy as np
from PIL import Image
import random

class FireSimulation:
    def __init__(self, image_path, cell_size=10, max_width=800, max_height=600, ignition_probability=0.05):
        self.image = Image.open(image_path).convert('L')
        self.cell_size = cell_size
        self.max_width = max_width
        self.max_height = max_height
        self.width, self.height = self.image.size
        self.grid = None
        self.ignition_probability = ignition_probability
        self.wind_strength = 0
        self.drought = False
        self.humidity = None
        self.elevation = None
        self.wind_map = None
        self.resize_image()
        self.create_grid()

    def resize_image(self):
        scale_factor = min(self.max_width / self.width, self.max_height / self.height)
        new_width = int(self.width * scale_factor)
        new_height = int(self.height * scale_factor)
        self.image = self.image.resize((new_width, new_height))
        self.width, self.height = new_width, new_height

    def create_grid(self):
        pixels = np.array(self.image)
        grid_width = self.width // self.cell_size
        grid_height = self.height // self.cell_size
        self.grid = np.zeros((grid_height, grid_width), dtype=int)
        self.humidity = np.random.uniform(0.3, 1.0, (grid_height, grid_width))
        self.elevation = np.random.randint(0, 255, (grid_height, grid_width))
        self.wind_map = np.random.uniform(0, 1, (grid_height, grid_width))

        for i in range(grid_height):
            for j in range(grid_width):
                block = pixels[i * self.cell_size:(i + 1) * self.cell_size, j * self.cell_size:(j + 1) * self.cell_size]
                avg = np.mean(block)
                if avg < 100: #teren zielony
                    self.grid[i, j] = 0
                elif avg < 200: #woda
                    self.grid[i, j] = 2
                else: #skała
                    self.grid[i, j] = 4

    def count_neighbors(self, x, y):
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        fire_neighbors = 0
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                if self.grid[nx, ny] == 1:
                    fire_neighbors += 1
        return fire_neighbors

    def update_grid(self):
        new_grid = np.copy(self.grid)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] == 0:
                    neighbor_count = self.count_neighbors(i, j)
                    ignition_factor = self.ignition_probability + self.wind_strength * self.wind_map[i, j] + (
                                1 - self.humidity[i, j])
                    ignition_factor += 0.1 * (self.elevation[i, j] / 255)

                    if self.elevation[i, j] > 200:
                        ignition_factor += 0.2

                    if neighbor_count > 0 and random.random() < ignition_factor:
                        new_grid[i, j] = 1
                elif self.grid[i, j] == 1:
                    new_grid[i, j] = 3
                elif self.grid[i, j] == 2:
                    new_grid[i, j] = 2
                elif self.grid[i, j] == 3:
                    new_grid[i, j] = 3
        self.grid = new_grid

    def ignite_fire_randomly(self):
        green_cells = [(i, j) for i in range(self.grid.shape[0]) for j in range(self.grid.shape[1]) if
                       self.grid[i, j] == 0]
        if green_cells:
            x, y = random.choice(green_cells)
            self.grid[x, y] = 1

    def place_dam(self):
        water_cells = [(i, j) for i in range(self.grid.shape[0]) for j in range(self.grid.shape[1]) if
                       self.grid[i, j] == 2]

        if water_cells:
            x, y = random.choice(water_cells)

            radius = random.randint(3, 5)

            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    distance = np.sqrt(dx ** 2 + dy ** 2)

                    if distance <= radius:
                        nx, ny = x + dx, y + dy

                        if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                            if self.grid[nx, ny] != 2:
                                self.grid[nx, ny] = 2
                            if self.grid[nx, ny] == 0:
                                self.grid[nx, ny] = 2

    def water_drop(self):
        fire_cells = [(i, j) for i in range(1, self.grid.shape[0] - 1)
                      for j in range(1, self.grid.shape[1] - 1) if self.grid[i, j] == 1]

        if fire_cells:
            x, y = random.choice(fire_cells)

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                        if self.grid[nx, ny] != 1 and self.grid[nx, ny] != 2:
                            self.grid[nx, ny] = 6

        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] == 6:
                    if random.random() < 0.05:
                      self.grid[i, j] = 5

    def increase_elevation(self):
        self.elevation = np.clip(self.elevation + 50, 0, 255)

    def controlled_burn(self): #wypalanie roślinności
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] == 0 and self.count_neighbors(i, j) > 0:
                    if random.random() < 0.3:
                        self.grid[i, j] = 5

    def render(self, screen, offset_x, offset_y):
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                color = (255, 255, 255)
                if self.grid[i, j] == 0: #roślinność
                    color = (0, 255, 0)
                elif self.grid[i, j] == 1: #ogień
                    color = (255, 0, 0)
                elif self.grid[i, j] == 2: #woda
                    color = (0, 0, 255)
                elif self.grid[i, j] == 3: #spalone
                    color = (169, 169, 169)
                elif self.grid[i, j] == 4: #skały
                    color = (128, 128, 128)
                elif self.grid[i, j] == 5: #ugaszone (ciemnozielone)
                    color = (0, 100, 0)
                elif self.grid[i, j] == 6: #ugaszone wodą
                    color = (0, 255, 255)
                pygame.draw.rect(screen, color,
                                 pygame.Rect(j * self.cell_size + offset_x, i * self.cell_size + offset_y,
                                             self.cell_size, self.cell_size))

        font = pygame.font.SysFont('Arial', 20)
        avg_humidity = np.mean(self.humidity)
        avg_elevation = np.mean(self.elevation)
        text_wind = font.render(f'Wiatr: {self.wind_strength:.2f}', True, (0, 0, 0))
        text_humidity = font.render(f'Wilgotność: {avg_humidity:.2f}', True, (0, 0, 0))
        text_elevation_label = font.render('Ukształtowanie', True, (0, 0, 0))
        text_elevation_value = font.render(f'terenu: {avg_elevation:.2f}', True, (0, 0, 0))
        screen.blit(text_wind, (20, 350))
        screen.blit(text_humidity, (20, 380))
        screen.blit(text_elevation_label, (20, 410))
        screen.blit(text_elevation_value, (20, 430))

    def increase_wind(self):
        self.wind_strength += 0.15

    def activate_drought(self):
        self.drought = True
        self.humidity = np.maximum(self.humidity - 0.2, 0.0)


def draw_buttons(screen):
    font = pygame.font.SysFont('Arial', 20)
    buttons = [
        ("Zrzut wody", (20, 50)),
        ("Tama", (20, 100)),
        ("Zwiększ wiatr", (20, 150)),
        ("Susza", (20, 200)),
        ("Wypal", (20, 250)),
        ("Teren górzysty", (20, 300))
    ]
    for text, pos in buttons:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pos[0], pos[1], 160, 40))
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (pos[0] + 10, pos[1] + 10))
    return buttons


def main():
    pygame.init()
    image_file_path = 'zbinaryzowany_obraz.bmp'
    simulation = FireSimulation(image_file_path, cell_size=10, ignition_probability=0.05)
    window_width = 1000
    window_height = 500
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Symulacja Pożaru Lasu')
    offset_x = 200
    offset_y = 0
    simulation.ignite_fire_randomly()
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((255, 255, 255))
        buttons = draw_buttons(screen)
        simulation.render(screen, offset_x, offset_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for idx, (text, pos) in enumerate(buttons):
                    if pos[0] <= mouse_x <= pos[0] + 160 and pos[1] <= mouse_y <= pos[1] + 40:
                        if idx == 0:  # Zrzut wody
                            simulation.water_drop()
                        elif idx == 1:  # Tama
                            simulation.place_dam()
                        elif idx == 2:  # Zwiększ wiatr
                            simulation.increase_wind()
                        elif idx == 3:  # Susza
                            simulation.activate_drought()
                        elif idx == 4:  # Wypal
                            simulation.controlled_burn()
                        elif idx == 5:  # Teren górzysty
                            simulation.increase_elevation()

        simulation.update_grid()
        pygame.display.flip()
        clock.tick(2)

    pygame.quit()

if __name__ == "__main__":
    main()
