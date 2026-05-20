import pygame
from system.audio_system import init_audio, play_move_sound, play_dog_hit_sound, play_cat_hit_sound
from entities.ebike import Ebike
from entities.obstacles.obstacles import Obstacles
from entities.obstacles.obs import ObstaclesEnum  
from core.settings import WIDTH, HEIGHT, FPS, ebike_size, life_points

# Import your road polygon definitions from settings
# Ensure these match your actual files
from core.settings import ROAD_A, ROAD_B, ROAD_C, ROAD_D

pygame.init()
init_audio()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E-Bike Game")

clock = pygame.time.Clock()

# ================= ROAD SETTINGS =================
# We group the coordinates into a list for easy drawing iterations
# Helper function to adjust coordinates if Y=0 needs to be the bottom of the screen
def map_coords(lane_coords):
    return [
        (x, HEIGHT if y == 0 else y) 
        for x, y in lane_coords
    ]

# Processed lane polygons
LANES_TO_DRAW = [
    map_coords(ROAD_A),
    map_coords(ROAD_B),
    map_coords(ROAD_C),
    map_coords(ROAD_D)
]

BORDER_WIDTH = 250
PLAYER_SIZE = ebike_size
life_remaining = life_points

# ================= LOAD OBJECTS =================
ebike = Ebike()
obstacle = Obstacles()

# ================= GAME LOOP =================
running = True

while running:

    dt = clock.tick(FPS)

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (life_remaining <= 0):
            running = False
        ebike.move(event, play_move_sound)

    # ================= DRAW =================
    screen.fill((135, 206, 235)) # Default background/landscape

    # 1. DRAW PERSPECTIVE ROADS (Using Polygons)
    # Alternating gray shades to make lane boundaries visible
    lane_colors = [(90, 90, 90), (95, 95, 95), (90, 90, 90), (95, 95, 95)]
    
    for i, lane_poly in enumerate(LANES_TO_DRAW):
        # Draw the solid lane surface
        pygame.draw.polygon(screen, lane_colors[i], lane_poly)
        # Draw a fine border around each lane to make them stand out
        pygame.draw.polygon(screen, (120, 120, 120), lane_poly, 2)

    # 2. DRAW PERSPECTIVE LANE SEPARATORS (Yellow dashed lines)
    # We trace along the internal shared edges of your road coordinates
    for i in range(len(LANES_TO_DRAW) - 1):
        # The shared point at the top (vanishing point)
        top_line_pt = LANES_TO_DRAW[i][2] 
        # The shared point at the bottom (foreground)
        bottom_line_pt = LANES_TO_DRAW[i][1] 
        pygame.draw.line(screen, (255, 255, 0), top_line_pt, bottom_line_pt, 4)

    # 3. DRAW BORDERS OUTSIDE THE ROAD
    # Left grass/dirt border
    left_border_poly = [(0, HEIGHT), (LANES_TO_DRAW[0][0][0], HEIGHT), (LANES_TO_DRAW[0][3][0], 180), (0, 180)]
    pygame.draw.polygon(screen, (126, 200, 80), left_border_poly)

    # Right grass/dirt border
    right_border_poly = [(LANES_TO_DRAW[3][1][0], HEIGHT), (WIDTH, HEIGHT), (WIDTH, 180), (LANES_TO_DRAW[3][2][0], 180)]
    pygame.draw.polygon(screen, (126, 200, 80), right_border_poly)

    # DRAW RANDOM OBSTACLE
    obstacle.draw(screen)

    # COLLISION DETECTION
    if ebike.is_colliding(obstacle):
        life_remaining -= 1
        if obstacle.type == ObstaclesEnum.DOG:
            play_dog_hit_sound()
        if obstacle.type == ObstaclesEnum.CAT:
            play_cat_hit_sound()
        obstacle.reset()

    # DRAW EBIKE
    ebike.draw(screen)

    pygame.display.flip()

pygame.quit()