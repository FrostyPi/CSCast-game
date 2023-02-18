import math

RESOLUTION = WIDTH, HEIGHT = 1024, 576
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2

FPS = 60
TILE_SIZE = 64

FOV = math.pi / 3
HALF_FOV = FOV / 2

RAY_COUNT = WIDTH // 8   #default was // 2
HALF_RAY_COUNT = RAY_COUNT // 2

d_ANGLE = FOV / RAY_COUNT
VISION_RANGE = 20
VISION_RANGE_ARC = 6