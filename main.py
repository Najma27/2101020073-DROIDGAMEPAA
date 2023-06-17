import pygame
import random
import math
import threading
from tkinter import messagebox
from tkinter import *
import time

# Inisialisasi pygame
pygame.init()

# Konfigurasi jendela permainan
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Droid Game_2101020073")
icon = pygame.image.load('001-droid.png')
pygame.display.set_icon(icon)

# Variabel global
cell_size = 40
droid_radius = cell_size // 2
red = (255, 0, 0)
green = (0, 255, 0)
teal = (0, 128, 128)
paused = False

# Variabel global peta
map_width = window_width // cell_size
map_height = window_height // cell_size
map_grid = [[0] * map_width for _ in range(map_height)]

# Variabel posisi droid
red_droid_positions = []

# Menggambar droid merah
def draw_red_droid():
    for pos in red_droid_positions:
        pygame.draw.circle(window, red, (pos[0] * cell_size + cell_size // 2, pos[1] * cell_size + cell_size // 2), droid_radius)

# Menggambar droid hijau
def draw_green_droid():
    pygame.draw.circle(window, green, (green_droid_pos[0] * cell_size + cell_size // 2, green_droid_pos[1] * cell_size + cell_size // 2), droid_radius)

# Fungsi untuk menampilkan pesan ketika droid merah menemukan droid hijau
def show_found_message():
    messagebox.showinfo("Droid Found", "Droid merah telah menemukan droid hijau!")

# Fungsi untuk mengacak posisi droid pada peta
def shuffle_positions():
    global red_droid_positions, green_droid_pos
    red_droid_positions = [(random.randint(0, map_width - 1), random.randint(0, map_height - 1))]
    green_droid_pos = (random.randint(0, map_width - 1), random.randint(0, map_height - 1))
    if red_droid_positions[0] == green_droid_pos:
        shuffle_positions()

# Fungsi untuk menghitung jarak antara dua posisi pada peta
def distance(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

# Fungsi untuk mendapatkan tetangga-tetangga dari suatu posisi pada peta
def get_neighbors(pos):
    neighbors = []
    x, y = pos

    if x > 0 and map_grid[y][x - 1] == 0:  # Tetangga di sebelah kiri
        neighbors.append((x - 1, y))
    if x < map_width - 1 and map_grid[y][x + 1] == 0:  # Tetangga di sebelah kanan
        neighbors.append((x + 1, y))
    if y > 0 and map_grid[y - 1][x] == 0:  # Tetangga di atas
        neighbors.append((x, y - 1))
    if y < map_height - 1 and map_grid[y + 1][x] == 0:  # Tetangga di bawah
        neighbors.append((x, y + 1))

    return neighbors

# Fungsi untuk melakukan algoritma A*
def astar():
    global red_droid_positions
    open_set = red_droid_positions.copy()
    came_from = {}
    g_score = {pos: 0 for pos in red_droid_positions}
    f_score = {pos: distance(pos, green_droid_pos) for pos in red_droid_positions}

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])

        if current == green_droid_pos:
            # Droid hijau ditemukan
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            path.append(green_droid_pos)

            # Munculkan pesan droid hijau ditemukan
            threading.Thread(target=show_found_message).start()

            # Tampilkan jalur yang ditempuh droid merah
            for pos in path:
                red_droid_positions.append(pos)
                window.fill((255, 255, 255))
                for i in range(map_width):
                    for j in range(map_height):
                        if map_grid[j][i] == 1:
                            pygame.draw.rect(window, teal, (i * cell_size, j * cell_size, cell_size, cell_size))
                draw_red_droid()
                draw_green_droid()
                pygame.display.update()
                time.sleep(0.5)

            break

        open_set.remove(current)

        for neighbor in get_neighbors(current):
            temp_g_score = g_score[current] + distance(current, neighbor)

            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + distance(neighbor, green_droid_pos)

                if neighbor not in open_set:
                    open_set.append(neighbor)

def astar_with_avoidance():
    global red_droid_positions
    open_set = red_droid_positions.copy()
    came_from = {}
    g_score = {pos: 0 for pos in red_droid_positions}
    f_score = {pos: distance(pos, green_droid_pos) for pos in red_droid_positions}

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])

        if current == green_droid_pos:
            # Droid hijau ditemukan
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            path.append(green_droid_pos)

            # Munculkan pesan droid hijau ditemukan
            threading.Thread(target=show_found_message).start()

            # Tampilkan jalur yang ditempuh droid merah
            for pos in path:
                red_droid_positions.append(pos)
                window.fill((255, 255, 255))
                for i in range(map_width):
                    for j in range(map_height):
                        if map_grid[j][i] == 1:
                            pygame.draw.rect(window, teal, (i * cell_size, j * cell_size, cell_size, cell_size))
                draw_red_droid()
                draw_green_droid()
                pygame.display.update()
                time.sleep(0.5)
            break

        open_set.remove(current)

        for neighbor in get_neighbors(current):
            temp_g_score = g_score[current] + distance(current, neighbor)

            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + distance(neighbor, green_droid_pos)

                if neighbor not in open_set:
                    open_set.append(neighbor)

# Fungsi untuk memulai permainan
def start_game():
    global red_droid_positions, green_droid_pos, run_astar, paused

    shuffle_positions()

    # Flag untuk menjalankan algoritma A*
    run_astar = False

    # Inisialisasi status pause
    paused = False

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update window
        window.fill((255, 255, 255))
        for i in range(map_width):
            for j in range(map_height):
                if map_grid[j][i] == 1:
                    pygame.draw.rect(window, teal, (i * cell_size, j * cell_size, cell_size, cell_size))
        draw_red_droid()
        draw_green_droid()
        pygame.display.update()

        # Jalankan algoritma A* jika flag run_astar bernilai True
        if run_astar:
            astar()
            run_astar = False

        # Jeda 0.1 detik
        time.sleep(0.1)

    # Berhenti pygame
    pygame.quit()
    quit()

# Fungsi untuk mengubah flag run_astar menjadi True saat tombol "Mulai" ditekan
def run_astar_algorithm():
    global run_astar
    run_astar = True

# Fungsi untuk mengacak peta
def shuffle_map():
    global map_grid
    map_grid = [[random.randint(0, 1) for _ in range(map_width)] for _ in range(map_height)]

# Fungsi untuk menambah droid merah
def add_red_droid():
    global red_droid_positions
    new_red_droid_pos = (random.randint(0, map_width - 1), random.randint(0, map_height - 1))
    if new_red_droid_pos != green_droid_pos and new_red_droid_pos not in red_droid_positions:
        red_droid_positions.append(new_red_droid_pos)

# Fungsi untuk menghapus droid merah
def remove_red_droid():
    global red_droid_positions
    if len(red_droid_positions) > 0:
        red_droid_positions.pop()

def shuffle_red_droid():
    global red_droid_positions
    new_red_droid_pos = (random.randint(0, map_width - 1), random.randint(0, map_height - 1))
    if new_red_droid_pos != green_droid_pos and new_red_droid_pos not in red_droid_positions:
        red_droid_positions = [new_red_droid_pos]

# Fungsi untuk mengacak posisi droid hijau
def shuffle_green_droid():
    global green_droid_pos
    green_droid_pos = (random.randint(0, map_width - 1), random.randint(0, map_height - 1))

def toggle_pause():
    global paused
    paused = not paused

# Fungsi untuk keluar dari permainan
def exit_game():
    pygame.quit()
    quit()

# Fungsi untuk menampilkan jendela GUI
def show_gui():
    root = Tk()
    root.title("Droid Game GUI_2101020073")
    root.geometry("200x200")

    start_button = Button(root, text="Mulai", command=run_astar_algorithm)
    start_button.pack()

    shuffle_map_button = Button(root, text="Acak Peta", command=shuffle_map)
    shuffle_map_button.pack()

    add_red_droid_button = Button(root, text="Tambah Droid Merah", command=add_red_droid)
    add_red_droid_button.pack()

    remove_red_droid_button = Button(root, text="Hapus Droid Merah", command=remove_red_droid)
    remove_red_droid_button.pack()

    shuffle_red_droid_button = Button(root, text="Acak Droid Merah", command=shuffle_red_droid)
    shuffle_red_droid_button.pack()

    shuffle_green_droid_button = Button(root, text="Acak Droid Hijau", command=shuffle_green_droid)
    shuffle_green_droid_button.pack()

    pause_button = Button(root, text="Pause", command=toggle_pause)
    pause_button.pack()

    exit_button = Button(root, text="Keluar", command=exit_game)
    exit_button.pack()

    root.mainloop()

# Thread untuk menampilkan jendela GUI
gui_thread = threading.Thread(target=show_gui)
gui_thread.start()

# Memulai permainan
start_game()