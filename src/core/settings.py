WIDTH = 1280
HEIGHT = 720
FPS = 60

NUM_LANES = 4
LANE_WIDTH = 195
ROAD_WIDTH = NUM_LANES * LANE_WIDTH
ROAD_X = (WIDTH - ROAD_WIDTH) // 2
LANE_CENTERS = [ROAD_X + (i * LANE_WIDTH) + (LANE_WIDTH // 2) for i in range(NUM_LANES)]

player_size = 64
player_x = WIDTH // 2
player_y = HEIGHT // 1.5
player_speed = 5
ebike_size = (128, 192)
obstacle_y_pos = HEIGHT // 4

obstacle_size = 64

life_points = 3
