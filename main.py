import pygame
import sys 

grid_s = 70
screen_s = 700
cell_s = screen_s/grid_s

#pausing
pause = False
pause_last = False

sd = 1

grid = [[0 for _ in range(grid_s)] for _ in range(grid_s)]
prev_grid = [row[:] for row in grid]

def draw_grid(screen):
    for y in range(grid_s):
        for x in range(grid_s):
            rect = pygame.Rect(x * cell_s, y * cell_s, cell_s, cell_s)
            color = (255, 255,  255) if grid[y][x] == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (150, 150, 150), rect, 1)

def buttons_func():
    global pause_last, pause
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        for y in range(grid_s):
            for x in range(grid_s):
                grid[y][x] = 0
    if keys[pygame.K_SPACE]:
        if not pause_last:
            pause = not pause
        pause_last = True
    else:
        pause_last = False

def update_cells():
    if pause == False:
        prev_grid = [row[:] for row in grid]
        for y in range(grid_s):
            for x in range(grid_s):
                if prev_grid[y][x] == 1: 
                    if find_naighbors(prev_grid, x ,y) < 2: 
                        grid[y][x] = 0
                    elif find_naighbors(prev_grid, x ,y) == 2 or find_naighbors(prev_grid, x ,y) == 3: 
                        grid[y][x] = 1
                    elif find_naighbors(prev_grid, x ,y) > 3: 
                        grid[y][x] = 0
                if prev_grid[y][x] == 0: 
                    if find_naighbors(prev_grid, x ,y) == 3: 
                        grid[y][x] = 1
                
                

def draw():
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:  # Left mouse button is held
        x, y = pygame.mouse.get_pos()
        grid[int(y / cell_s)][int(x / cell_s)] = 1
    if pressed[2]:  # Left mouse button is held
        x, y = pygame.mouse.get_pos()
        grid[int(y / cell_s)][int(x / cell_s)] = 0

def find_naighbors(two_d_array, x ,y):
    height = len(two_d_array)
    width = len(two_d_array[0])
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # skip the center cell itself
            nx = (x + dx) % width
            ny = (y + dy) % height
            if two_d_array[ny][nx] == 1:
                count += 1
    return count


pygame.init()
screen = pygame.display.set_mode((screen_s, screen_s))
pygame.display.set_caption("Cellular Automaton Grid")

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid(screen)
    pygame.display.flip()

    clock.tick(40) # Slowed down for easier viewing

    buttons_func()
    update_cells()
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
