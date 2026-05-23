import pygame
import sys
import cv2
import numpy as np
from system.audio_system import init_audio, play_move_sound, play_bato_hit_sound, play_dog_hit_sound, play_cat_hit_sound, play_in_game_music
from entities.ebike import Ebike
from entities.obstacles.obstacles import Obstacles
from entities.obstacles.obs import ObstaclesEnum
from core.settings import WIDTH, HEIGHT, FPS, ebike_size, life_points

# Scene Function Imports
from scenes.game_scene import in_game_scene, pause_menu, game_over, game_menu, get_player_name, leaderboard, reset_save_flag
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
menu_image = pygame.image.load('src/assets/game_menu1.png').convert_alpha()
pause_image = pygame.image.load('src/assets/game_pause1.png').convert_alpha()
leaderboard_image = pygame.image.load('src/assets/leaderboard.png').convert_alpha()

# ================= VIDEO INITIALIZATION =================
game_bg_video = cv2.VideoCapture('src/assets/game_bg.mp4')
game_bg_fps = game_bg_video.get(cv2.CAP_PROP_FPS)

# ================= ROUTING CONTEXT MANAGEMENT SYSTEM =================
current_state = 'MENU'
life_remaining = life_points
player_name = None
pending_name = ""

def reset_full_game_state():
    """Restores full variable structures to defaults upon fresh state instantiation request."""
    global life_remaining, current_state, ebike, obstacle, score_system
    life_remaining = life_points
    ebike = Ebike()
    obstacle = Obstacles()
    score_system = ScoreSystem()
    current_state = 'PLAY'
    reset_save_flag()

# ================= CENTRAL APPLICATION LOOP =================
running = True

while running:
    dt = clock.tick(FPS)

    # ================= UNIVERSAL INPUT HANDLING INTERACTION LAYER =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if current_state == 'PLAY':
                if event.key == pygame.K_SPACE:
                    current_state = 'PAUSE'

            elif current_state == 'PAUSE':
                if event.key == pygame.K_SPACE:
                    current_state = 'PLAY'
                elif event.key == pygame.K_ESCAPE:
                    current_state = 'MENU'

            elif current_state == 'MENU':
                play_in_game_music()
                if event.key == pygame.K_RETURN:
                    current_state = 'NAME_INPUT'
                    pending_name = ""
                elif event.key == pygame.K_l:
                    current_state = 'LEADERBOARD'
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif current_state == 'NAME_INPUT':
                if event.key == pygame.K_RETURN:
                    player_name = pending_name.strip() or 'PLAYER'
                    reset_full_game_state()
                elif event.key == pygame.K_BACKSPACE:
                    pending_name = pending_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    current_state = 'MENU'
                elif event.unicode and event.unicode.isprintable() and len(pending_name) < 16:
                    pending_name += event.unicode

            elif current_state == 'GAME_OVER':
                if event.key == pygame.K_r:
                    reset_full_game_state()
                    current_state = 'MENU'
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif current_state == 'LEADERBOARD':
                if event.key == pygame.K_ESCAPE:
                    current_state = 'MENU'

    # ================= SMOOTH INPUT & UPDATE =================
    if current_state == 'PLAY':
        ebike.handle_input(play_move_sound)
        ebike.update()

    # ================= APPLICATION ROUTING EXECUTIVE LAYER =================
    if current_state == 'PLAY':
        collision_detected = in_game_scene(
            screen, clock, dt, ebike, obstacle, score_system, font,
            delarosa_img, LANES_TO_DRAW, WIDTH, HEIGHT, game_bg_video
        )

        if collision_detected:
            if obstacle.hit_type == ObstaclesEnum.BATO:
                play_bato_hit_sound()
            elif obstacle.hit_type == ObstaclesEnum.DOG:
                play_dog_hit_sound()
            elif obstacle.hit_type == ObstaclesEnum.CAT:
                play_cat_hit_sound()
            life_remaining -= 1
            if life_remaining <= 0:
                current_state = 'GAME_OVER'

        score_system.draw(screen, font)
        for i in range(life_remaining):
            screen.blit(delarosa_img, (20 + (i * 50), 60))

    elif current_state == 'PAUSE':
        pause_menu(screen, font, WIDTH, HEIGHT, pause_image)

    elif current_state == 'MENU':
        game_menu(screen, font, WIDTH, HEIGHT, menu_image)

    elif current_state == 'LEADERBOARD':
        leaderboard(screen, font, WIDTH, HEIGHT, leaderboard_image)

    elif current_state == 'NAME_INPUT':
        get_player_name(screen, font, WIDTH, HEIGHT, menu_image, pending_name)

    elif current_state == 'GAME_OVER':
        game_over(screen, font, score_system, WIDTH, HEIGHT, player_name)

    pygame.display.flip()

play_in_game_music()
game_bg_video.release()
pygame.quit()
sys.exit()