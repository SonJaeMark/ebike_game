import pygame
from system.audio_system import init_audio, play_move_sound, play_dog_hit_sound, play_cat_hit_sound
from entities.ebike import Ebike
from entities.obstacles.obstacles import Obstacles
from entities.obstacles.obs import ObstaclesEnum  
from core.settings import WIDTH, HEIGHT, FPS, ebike_size, life_points

# Import your road polygon definitions from settings
from core.settings import ROAD_A, ROAD_B, ROAD_C, ROAD_D, difficulty_speed_base

pygame.init()
init_audio()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E-Bike Game")

clock = pygame.time.Clock()

# ================= ROAD SETTINGS =================
def map_coords(lane_coords):
    return [
        (x, HEIGHT if y == 0 else y) 
        for x, y in lane_coords
    ]

LANES_TO_DRAW = [
    map_coords(ROAD_A),
    map_coords(ROAD_B),
    map_coords(ROAD_C),
    map_coords(ROAD_D)
]

BORDER_WIDTH = 250
PLAYER_SIZE = ebike_size
life_remaining = life_points

# --- LANE ANIMATION CONFIGURATION ---
road_offset = 0.0
road_speed = difficulty_speed_base  # Increase to go faster, decrease to go slower

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

    # --- Update Road Animation State ---
    # Convert speed relative to frame rate to maintain consistency
    road_offset += (road_speed * (dt / 1000.0))
    if road_offset >= 1.0:
        road_offset -= 1.0

    # ================= DRAW =================
    screen.fill((135, 206, 235)) # Sky/Landscape Backdrop

    # 1. DRAW PERSPECTIVE ROADS (Using Polygons)
    lane_colors = [(90, 90, 90), (95, 95, 95), (90, 90, 90), (95, 95, 95)]
    for i, lane_poly in enumerate(LANES_TO_DRAW):
        pygame.draw.polygon(screen, lane_colors[i], lane_poly)
        pygame.draw.polygon(screen, (120, 120, 120), lane_poly, 2)

    # 2. DRAW ANIMATED PERSPECTIVE LANE SEPARATORS (Yellow dashed lines)
    num_dashes = 6  # Number of visible dash steps along the line
    
    for i in range(len(LANES_TO_DRAW) - 1):
        # Establish Vector structures for precision interpolation calculations
        top_line_pt = pygame.math.Vector2(LANES_TO_DRAW[i][2]) 
        bottom_line_pt = pygame.math.Vector2(LANES_TO_DRAW[i][1]) 
        
        # Look ahead and behind by 1 index to prevent clipping artifacts at edge boundaries
        for j in range(-1, num_dashes + 1):
            # Calculate linear start/end position of the current dash chunk
            t_start = (j + road_offset) / num_dashes
            t_end = (j + road_offset + 0.4) / num_dashes  # 0.4 determines dash visual spacing
            
            # Confine math bounds safely within vector tracking spaces
            t_start = max(0.0, min(1.0, t_start))
            t_end = max(0.0, min(1.0, t_end))
            
            # Squaring the values applies a perspective warp (exponentially faster near bottom)
            p_start = t_start ** 2
            p_end = t_end ** 2
            
            # Map tracking points along the lane boundary line
            start_draw_pt = top_line_pt.lerp(bottom_line_pt, p_start)
            end_draw_pt = top_line_pt.lerp(bottom_line_pt, p_end)
            
            # Dynamically increase dash stroke width as it moves closer to foreground
            line_thickness = int(3 + (p_start * 7))
            
            if p_start < p_end:
                pygame.draw.line(screen, (255, 255, 0), start_draw_pt, end_draw_pt, line_thickness)

    # 3. DRAW BORDERS OUTSIDE THE ROAD
    left_border_poly = [(0, HEIGHT), (LANES_TO_DRAW[0][0][0], HEIGHT), (LANES_TO_DRAW[0][3][0], 180), (0, 180)]
    pygame.draw.polygon(screen, (126, 200, 80), left_border_poly)

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
