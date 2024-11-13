import os
import tkinter as tk
from tkinter import ttk
import random
import time

# Zmienne środowiskowe
os.environ['TCL_LIBRARY'] = r'C:\Users\emili\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\emili\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

class GameOfLife:
    def __init__(self, root, size=200, cell_size=4):
        self.size = size
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.root = root
        self.canvas = tk.Canvas(root, width=size * cell_size, height=size * cell_size, bg="white")
        self.canvas.pack(pady=20, side=tk.RIGHT)
        self.boundary_condition = 'periodic'

    def set_boundary_condition(self, condition):
        self.boundary_condition = condition

    def set_initial_state(self, state_type, count=5):
        if state_type == 'Glider':
            self.grid = self.create_glider(count)
        elif state_type == 'Oscillator':
            self.grid = self.create_oscillator(count)
        elif state_type == 'Random':
            self.grid = self.create_random(count)
        elif state_type == 'Static':
            self.grid = self.create_static(count)

    def create_glider(self, count=1):
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for _ in range(count):
            x = random.randint(1, self.size - 3)
            y = random.randint(1, self.size - 3)
            grid[x][y + 1] = 1
            grid[x + 1][y + 2] = 1
            grid[x + 2][y] = 1
            grid[x + 2][y + 1] = 1
            grid[x + 2][y + 2] = 1
        return grid

    def create_oscillator(self, count=5):
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

        for _ in range(count):
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            grid[x][y - 1] = 1
            grid[x][y] = 1
            grid[x][y + 1] = 1

        return grid

    def create_random(self, count=5):
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for _ in range(count):
            x = random.randint(1, self.size - 1)
            y = random.randint(1, self.size - 1)
            grid[x][y] = 1
        return grid

    def create_static(self, count=1):
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for _ in range(count):
            x = random.randint(1, self.size - 4)
            y = random.randint(1, self.size - 4)

            grid[x][y + 1] = 1
            grid[x][y + 2] = 1
            grid[x + 1][y] = 1
            grid[x + 1][y + 3] = 1
            grid[x + 2][y + 1] = 1
            grid[x + 2][y + 2] = 1

        return grid

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 1:
                    x1 = j * self.cell_size
                    y1 = i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def count_neighbors(self, x, y):
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if self.boundary_condition == 'periodic':
                nx = nx % self.size
                ny = ny % self.size
            elif self.boundary_condition == 'reflective':
                if nx < 0 or ny < 0 or nx >= self.size or ny >= self.size:
                    continue
            count += self.grid[nx][ny]
        return count

    def update_grid(self):
        new_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    new_grid[i][j] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[i][j] = 1 if neighbors == 3 else 0
        self.grid = new_grid

    def run_simulation(self, steps=15, delay=100):
        for _ in range(steps):
            self.draw_grid()
            self.update_grid()
            self.root.update_idletasks()
            self.root.update()
            time.sleep(delay / 1000)


def start_simulation(app, condition, initial_state, count):
    app.set_boundary_condition(condition)
    app.set_initial_state(initial_state, count)
    app.run_simulation(steps=100, delay=100)


if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("1000x650")

    app = GameOfLife(root, size=200, cell_size=5)

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.LEFT, padx=10, pady=10)

    label = tk.Label(control_frame, text="Wybierz warunek graniczny:")
    label.grid(row=0, column=0, padx=5)

    boundary_options = ttk.Combobox(control_frame, values=["periodic", "reflective"])
    boundary_options.set("periodic")
    boundary_options.grid(row=0, column=1, padx=5)

    label_state = tk.Label(control_frame, text="Wybierz stan początkowy:")
    label_state.grid(row=1, column=0, padx=5)

    state_options = ttk.Combobox(control_frame, values=["Glider", "Oscillator", "Random", "Static"])
    state_options.set("Glider")
    state_options.grid(row=1, column=1, padx=5)

    label_count = tk.Label(control_frame, text="Liczba komórek:")
    label_count.grid(row=2, column=0, padx=5)

    count_entry = tk.Entry(control_frame)
    count_entry.insert(0, "5")
    count_entry.grid(row=2, column=1, padx=5)

    start_button = tk.Button(control_frame, text="Start",
                             command=lambda: start_simulation(app, boundary_options.get(), state_options.get(),
                                                              int(count_entry.get())))
    start_button.grid(row=0, column=2, rowspan=3, padx=5)

    root.mainloop()
