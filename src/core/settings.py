import pygame

WIDTH = 1280
HEIGHT = 720
FPS = 60

NUM_LANES = 4
LANE_WIDTH = 195
ROAD_WIDTH = NUM_LANES * LANE_WIDTH
ROAD_X = (WIDTH - ROAD_WIDTH) // 2
LANE_CENTERS = [ROAD_X + (i * LANE_WIDTH) + (LANE_WIDTH // 2) for i in range(NUM_LANES)]

# Road polygon definitions (Bottom-Left, Bottom-Right, Top-Right, Top-Left)
ROAD_A = ((250.0, 0), (445.0, 0), (591.25, 180), (542.5, 180))
ROAD_B = ((445.0, 0), (640.0, 0), (640.00, 180), (591.25, 180))
ROAD_C = ((640.0, 0), (835.0, 0), (688.75, 180), (640.00, 180))
ROAD_D = ((835.0, 0), (1030.0, 0), (737.50, 180), (688.75, 180))

LANE_A_CENTERLINE = (pygame.math.Vector2(566.875, 180), pygame.math.Vector2(347.5, HEIGHT))
LANE_B_CENTERLINE = (pygame.math.Vector2(615.625, 180), pygame.math.Vector2(542.5, HEIGHT))
LANE_C_CENTERLINE = (pygame.math.Vector2(664.375, 180), pygame.math.Vector2(737.5, HEIGHT))
LANE_D_CENTERLINE = (pygame.math.Vector2(713.125, 180), pygame.math.Vector2(932.5, HEIGHT))

LANES = [LANE_A_CENTERLINE, LANE_B_CENTERLINE, LANE_C_CENTERLINE, LANE_D_CENTERLINE]

EBIKE_LANE_A_CENTERLINE = (566.88, 100)
EBIKE_LANE_B_CENTERLINE = (615.62, 100)
EBIKE_LANE_C_CENTERLINE = (664.38, 100)
EBIKE_LANE_D_CENTERLINE = (713.12, 100)

difficulty_speed_multiplier = 2
difficulty_speed_base = 2.0

player_size = 64
player_x = WIDTH // 2
player_y = HEIGHT // 1.5
player_speed = 5
ebike_size = (128, 192)
obstacle_y_pos = HEIGHT // 4

obstacle_size = 64

life_points = 3