import pygame
import sys
from system.audio_system import init_audio, play_move_sound
from entities.ebike import Ebike
from entities.obstacles.obstacles import Obstacles
from entities.obstacles.obs import ObstaclesEnum
from core.settings import WIDTH, HEIGHT, FPS, ebike_size, life_points

# Scene Function Imports
from scenes.game_scene import in_game_scene, pause_menu, game_over, reset_save_flag
from system.scoring_system import ScoreSystem
from core.settings import ROAD_A, ROAD_B, ROAD_C, ROAD_D

pygame.init()
init_audio()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E-Bike Game")
clock = pygame.time.Clock()

# ================= ROAD CONFIG GENERATORS =================
def map_coords(lane_coords):
    return [(x, HEIGHT if y == 0 else y) for x, y in lane_coords]

LANES_TO_DRAW = [map_coords(ROAD_A), map_coords(ROAD_B), map_coords(ROAD_C), map_coords(ROAD_D)]

# ================= OBJECT STACK INSTANTIATION =================
ebike = Ebike()
obstacle = Obstacles()
score_system = ScoreSystem()
font = pygame.font.SysFont('Arial', 36)

delarosa_img = pygame.image.load('src/assets/images/delarosa.webp').convert_alpha()
delarosa_img = pygame.transform.scale(delarosa_img, (40, 40))

# ================= ROUTING CONTEXT MANAGEMENT SYSTEM =================
current_state = 'PLAY'
life_remaining = life_points

def reset_full_game_state():
    """Restores full variable structures to defaults upon fresh state instantiation request."""
    global life_remaining, current_state, ebike, obstacle, score_system
    life_remaining = life_points
    ebike = Ebike()
    obstacle = Obstacles()
    score_system = ScoreSystem()
    current_state = 'PLAY'
    reset_save_flag()  # Allow next game over to save again

# ================= CENTRAL APPLICATION LOOP =================
running = True

while running:
    dt = clock.tick(FPS)

    # ================= UNIVERSAL INPUT HANDLING INTERACTION LAYER =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # 1. PLAY STATE CONTROLS
            if current_state == 'PLAY':
                if event.key == pygame.K_SPACE:
                    current_state = 'PAUSE'
                # else:
                #     ebike.move(event, play_move_sound)   # <--- In-comment ko muna (old code)

            # 2. PAUSE STATE CONTROLS
            elif current_state == 'PAUSE':
                if event.key == pygame.K_SPACE:
                    current_state = 'PLAY'

            # 3. GAME OVER STATE CONTROLS
            elif current_state == 'GAME_OVER':
                if event.key == pygame.K_r:
                    reset_full_game_state()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # ================= BAGONG IDINAGDAG - SMOOTH INPUT & UPDATE =================
    if current_state == 'PLAY':
        ebike.handle_input(play_move_sound)   # Responsive A/D at Left/Right
        ebike.update()                        # Smooth lane transition

    # ================= APPLICATION ROUTING EXECUTIVE LAYER =================
    if current_state == 'PLAY':
        collision_detected = in_game_scene(
            screen, clock, dt, ebike, obstacle, score_system, font,
            delarosa_img, LANES_TO_DRAW, WIDTH, HEIGHT
        )

        if collision_detected:
            life_remaining -= 1
            if life_remaining <= 0:
                current_state = 'GAME_OVER'

        score_system.draw(screen, font)
        for i in range(life_remaining):
            screen.blit(delarosa_img, (20 + (i * 50), 60))

    elif current_state == 'PAUSE':
        pause_menu(screen, font, WIDTH, HEIGHT)

    elif current_state == 'GAME_OVER':
        game_over(screen, font, score_system, WIDTH, HEIGHT)

    pygame.display.flip()

pygame.quit()
sys.exit()