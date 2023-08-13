import numpy as np
import pygame
import sys
import math

WALL = 1
EMPTY = 0
NUM_OF_RANDOM_WALLS = 4
FILL_COLOR = (0, 0, 0)

WINDOW_HEIGHT = 480
WINDOW_WIDTH = WINDOW_HEIGHT * 2
MAP_SIZE = 16
TILE_SIZE = ((WINDOW_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = WINDOW_WIDTH / CASTED_RAYS

posX = (WINDOW_WIDTH / 2) / 2
posY = (WINDOW_WIDTH / 2) / 2
angle = math.pi
WALL_HEIGHT = 30000
ROTATION_SPEED = 0.1
MOVEMENT_SPEED = 5

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Raycasting")
CLOCK = pygame.time.Clock()


def generate_map():
    grid = np.zeros((MAP_SIZE, MAP_SIZE))
    for x in range(NUM_OF_RANDOM_WALLS):
        random_col = np.random.randint(0, MAP_SIZE - 1)
        random_row = np.random.randint(0, MAP_SIZE - 1)

        grid[random_col, random_row] = WALL

    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            grid[0, y] = WALL
            grid[x, 0] = WALL
            grid[MAP_SIZE - 1, y] = WALL
            grid[x, MAP_SIZE - 1] = WALL

    mapString = ""
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            mapString += str(int(grid[x, y]))

    return mapString


def cast_rays():
    start_angle = angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = posX - math.sin(start_angle) * depth
            target_y = posY + math.cos(start_angle) * depth
            X = int(target_x / TILE_SIZE)
            Y = int(target_y / TILE_SIZE)

            pos = Y * MAP_SIZE + X

            if MAP[pos] == str(WALL):
                color = int(50 / (1 + depth * depth * 0.0001))

                depth *= math.cos(angle - start_angle)

                wall_height = WALL_HEIGHT / (depth + 0.0001)

                if wall_height > WINDOW_HEIGHT:
                    wall_height = WINDOW_HEIGHT

                pygame.draw.rect(SCREEN, (color, color, color), (
                    ray * SCALE, (WINDOW_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))

                break

        start_angle += STEP_ANGLE


MAP = generate_map()
IS_FORWARD = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    col = int(posX / TILE_SIZE)
    row = int(posY / TILE_SIZE)

    square = row * MAP_SIZE + col

    if MAP[square] == str(WALL):
        if IS_FORWARD:
            posX -= -math.sin(angle) * MOVEMENT_SPEED
            posY -= math.cos(angle) * MOVEMENT_SPEED
        else:
            posX += -math.sin(angle) * MOVEMENT_SPEED
            posY += math.cos(angle) * MOVEMENT_SPEED

    SCREEN.fill(FILL_COLOR)
    cast_rays()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        angle -= ROTATION_SPEED
    if keys[pygame.K_RIGHT]:
        angle += ROTATION_SPEED
    if keys[pygame.K_UP]:
        IS_FORWARD = True
        posX += -math.sin(angle) * MOVEMENT_SPEED
        posY += math.cos(angle) * MOVEMENT_SPEED
    if keys[pygame.K_DOWN]:
        IS_FORWARD = False
        posX -= -math.sin(angle) * MOVEMENT_SPEED
        posY -= math.cos(angle) * MOVEMENT_SPEED

    CLOCK.tick(60)

    pygame.display.flip()
