import pygame
from system.audio_system import init_audio, play_move_sound, play_dog_hit_sound, play_cat_hit_sound
from entities.ebike import Ebike
from entities.obstacles.obstacles import Obstacles
from entities.obstacles.obs import ObstaclesEnum  
from core.settings import WIDTH, HEIGHT, FPS, ebike_size, life_points
from system.scoring_system import ScoreSystem

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

road_offset = 0.0
road_speed = difficulty_speed_base

# ================= LOAD OBJECTS =================
ebike = Ebike()
obstacle = Obstacles()
score_system = ScoreSystem()
font = pygame.font.SysFont('Arial', 36)

# ================= LOAD LIFE INDICATOR =================
delarosa_img = pygame.image.load('src/assets/images/delarosa.webp').convert_alpha()
delarosa_img = pygame.transform.scale(delarosa_img, (40, 40))

# ================= GAME LOOP =================
running = True

while running:

    dt = clock.tick(FPS)
    score_system.update(dt)

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ebike.move(event, play_move_sound)

    # Check lives
    if life_remaining <= 0:
        running = False

    # --- Update Road Animation ---
    road_offset += (road_speed * (dt / 1000.0))
    if road_offset >= 1.0:
        road_offset -= 1.0

    # ================= DRAW =================
    screen.fill((135, 206, 235))

    # 1. DRAW PERSPECTIVE ROADS
    lane_colors = [(90, 90, 90), (95, 95, 95), (90, 90, 90), (95, 95, 95)]
    for i, lane_poly in enumerate(LANES_TO_DRAW):
        pygame.draw.polygon(screen, lane_colors[i], lane_poly)
        pygame.draw.polygon(screen, (120, 120, 120), lane_poly, 2)

    # 2. DRAW ANIMATED LANE SEPARATORS
    num_dashes = 6

    for i in range(len(LANES_TO_DRAW) - 1):
        top_line_pt = pygame.math.Vector2(LANES_TO_DRAW[i][2])
        bottom_line_pt = pygame.math.Vector2(LANES_TO_DRAW[i][1])

        for j in range(-1, num_dashes + 1):
            t_start = (j + road_offset) / num_dashes
            t_end = (j + road_offset + 0.4) / num_dashes

            t_start = max(0.0, min(1.0, t_start))
            t_end = max(0.0, min(1.0, t_end))

            p_start = t_start ** 2
            p_end = t_end ** 2

            start_draw_pt = top_line_pt.lerp(bottom_line_pt, p_start)
            end_draw_pt = top_line_pt.lerp(bottom_line_pt, p_end)

            line_thickness = int(3 + (p_start * 7))

            if p_start < p_end:
                pygame.draw.line(screen, (255, 255, 0), start_draw_pt, end_draw_pt, line_thickness)

    # 3. DRAW BORDERS
    left_border_poly = [(0, HEIGHT), (LANES_TO_DRAW[0][0][0], HEIGHT), (LANES_TO_DRAW[0][3][0], 180), (0, 180)]
    pygame.draw.polygon(screen, (126, 200, 80), left_border_poly)

    right_border_poly = [(LANES_TO_DRAW[3][1][0], HEIGHT), (WIDTH, HEIGHT), (WIDTH, 180), (LANES_TO_DRAW[3][2][0], 180)]
    pygame.draw.polygon(screen, (126, 200, 80), right_border_poly)

    # DRAW RANDOM OBSTACLE
    obstacle.draw(screen)

    # COLLISION DETECTION
    if ebike.is_colliding(obstacle):
        if obstacle.type == ObstaclesEnum.DOG:
            play_dog_hit_sound()
        if obstacle.type == ObstaclesEnum.CAT:
            play_cat_hit_sound()
        life_remaining -= 1
        obstacle.reset()
    else:
        if obstacle.rect.y > HEIGHT:
            score_system.add_dodge_bonus()

    # DRAW EBIKE
    ebike.draw(screen)

    # DRAW HUD
    score_system.draw(screen, font)
    for i in range(life_remaining):
        screen.blit(delarosa_img, (20 + (i * 50), 60))

    pygame.display.flip()

pygame.quit()