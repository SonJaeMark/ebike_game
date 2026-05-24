import json
import os
import pygame
import cv2
import numpy as np
from system.audio_system import init_audio, play_dog_hit_sound, play_cat_hit_sound, play_game_over_music, stop_game_over_music
from entities.obstacles.obs import ObstaclesEnum

_score_saved = False
_game_over_music_playing = False

def save_score_once(score_system, player_name):
    global _score_saved
    if not _score_saved:
        score_system.save_to_leaderboard(player_name)
        _score_saved = True

def reset_save_flag():
    global _score_saved, _game_over_music_playing
    _score_saved = False
    _game_over_music_playing = False
    stop_game_over_music()

def play_game_over_music_once():
    global _game_over_music_playing
    if not _game_over_music_playing:
        play_game_over_music()
        _game_over_music_playing = True

def in_game_scene(screen, clock, dt, ebike, obstacles, score_system, font, delarosa_img, LANES_TO_DRAW, WIDTH, HEIGHT, game_bg_video, level=1):
    global road_offset
    if 'road_offset' not in globals():
        globals()['road_offset'] = 0.0
    
    
    # base road speed; doubled in level 3
    road_speed = 1.0 * (2 if level == 3 else 1)
    
    score_system.update(dt)
    globals()['road_offset'] += (road_speed * (dt / 1000.0))
    if globals()['road_offset'] >= 1.0:
        globals()['road_offset'] -= 1.0

    # Read and display video background
    ret, frame = game_bg_video.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = np.transpose(frame, (1, 0, 2))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), (HEIGHT, WIDTH), "RGB")
        screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))
        # speed up video playback for level 3 by advancing one extra frame
        if level == 3:
            try:
                game_bg_video.grab()
            except Exception:
                pass
    else:
        # Loop video
        game_bg_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = game_bg_video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frame = np.transpose(frame, (1, 0, 2))
            frame_surface = pygame.image.frombuffer(frame.tobytes(), (HEIGHT, WIDTH), "RGB")
            screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))
            if level == 3:
                try:
                    game_bg_video.grab()
                except Exception:
                    pass

    # ================= ROAD CONFIGURATION =================
    # Commented out: road and left/right green borders
    # lane_colors = [(90, 90, 90), (95, 95, 95), (90, 90, 90), (95, 95, 95)]
    # for i, lane_poly in enumerate(LANES_TO_DRAW):
    #     pygame.draw.polygon(screen, lane_colors[i], lane_poly)
    #     pygame.draw.polygon(screen, (120, 120, 120), lane_poly, 2)

    # ================= ROAD LINES (Yellow Dashes) =================

    num_dashes = 6
    for i in range(len(LANES_TO_DRAW) - 1):
        top_line_pt = pygame.math.Vector2(LANES_TO_DRAW[i][2]) 
        bottom_line_pt = pygame.math.Vector2(LANES_TO_DRAW[i][1]) 
        
        for j in range(-1, num_dashes + 1):
            t_start = (j + globals()['road_offset']) / num_dashes
            t_end = (j + globals()['road_offset'] + 0.4) / num_dashes
            
            t_start = max(0.0, min(1.0, t_start))
            t_end = max(0.0, min(1.0, t_end))
            
            p_start = t_start ** 2
            p_end = t_end ** 2
            
            start_draw_pt = top_line_pt.lerp(bottom_line_pt, p_start)
            end_draw_pt = top_line_pt.lerp(bottom_line_pt, p_end)
            
            line_thickness = int(3 + (p_start * 7))
            if p_start < p_end:
                pygame.draw.line(screen, (255, 255, 0), start_draw_pt, end_draw_pt, line_thickness)

    left_border_poly = [(0, HEIGHT), (LANES_TO_DRAW[0][0][0], HEIGHT), (LANES_TO_DRAW[0][3][0], 180), (0, 180)]
    # pygame.draw.polygon(screen, (126, 200, 80), left_border_poly)

    right_border_poly = [(LANES_TO_DRAW[3][1][0], HEIGHT), (WIDTH, HEIGHT), (WIDTH, 180), (LANES_TO_DRAW[3][2][0], 180)]
    # pygame.draw.polygon(screen, (126, 200, 80), right_border_poly)

    # Support multiple obstacles: `obstacles` is expected to be a list
    for obs in obstacles:
        old_y = obs.rect.y
        obs.draw(screen)

        if old_y <= HEIGHT and obs.rect.y < old_y:
            score_system.add_dodge_bonus()

        if ebike.is_colliding(obs):
            hit_type = obs.type
            obs.reset()
            return hit_type

    ebike.draw(screen)
    return None

def pause_menu(screen, font, WIDTH, HEIGHT, pause_image):
    screen.fill((0, 0, 0))
    if pause_image:
        pause_surface = pygame.transform.smoothscale(pause_image, (WIDTH, HEIGHT))
        screen.blit(pause_surface, (0, 0))

def game_over(screen, font, score_system, WIDTH, HEIGHT, player_name, game_over_video):
    """Game Over terminal state rendering layout with video background."""
    save_score_once(score_system, player_name)
    play_game_over_music_once()

    # Read and display the game over video background
    ret, frame = game_over_video.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), (WIDTH, HEIGHT), "RGB")
        screen.blit(frame_surface, (0, 0))
    else:
        game_over_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = game_over_video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            frame_surface = pygame.image.frombuffer(frame.tobytes(), (WIDTH, HEIGHT), "RGB")
            screen.blit(frame_surface, (0, 0))
    score_text = font.render(str(score_system.score), True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))

def game_menu(screen, font, WIDTH, HEIGHT, menu_image):
    """Render the opening menu with the menu image."""
    screen.fill((0, 0, 0))

    if menu_image:
        menu_surface = pygame.transform.smoothscale(menu_image, (WIDTH, HEIGHT))
        screen.blit(menu_surface, (0, 0))

def leaderboard(screen, font, WIDTH, HEIGHT, leaderboard_image):
    screen.fill((0, 0, 0))
    if leaderboard_image:
        bg = pygame.transform.smoothscale(leaderboard_image, (WIDTH, HEIGHT))
        screen.blit(bg, (0, 0))

    data_path = os.path.join(os.path.dirname(__file__), '../../data/leaderboard.json')
    scores = []
    if os.path.exists(data_path):
        try:
            with open(data_path, 'r') as f:
                scores = json.load(f)
        except (json.JSONDecodeError, OSError):
            scores = []

    if not isinstance(scores, list):
        scores = []

    scores = [entry for entry in scores if isinstance(entry, dict) and 'score' in entry]
    scores.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_scores = scores[:10]

    

    row_y = 140
    label_font = pygame.font.SysFont('Arial', 28)
    if not top_scores:
        no_scores_text = label_font.render('No scores yet.', True, (204, 0, 0))
        screen.blit(no_scores_text, (WIDTH // 2 - no_scores_text.get_width() // 2, row_y))
    else:
        for index, entry in enumerate(top_scores, start=1):
            name = entry.get('name', 'PLAYER')
            score = entry.get('score', 0)
            row_text = label_font.render(f'{index}. {name} - {score}', True, (204, 0, 0))
            screen.blit(row_text, (WIDTH // 2 - row_text.get_width() // 2, row_y))
            row_y += 38

    


def get_player_name(screen, font, WIDTH, HEIGHT, menu_image, player_name):
    """Render the player name entry scene."""
    screen.fill((0, 0, 0))

    if menu_image:
        menu_surface = pygame.transform.smoothscale(menu_image, (WIDTH, HEIGHT))
        screen.blit(menu_surface, (0, 0))

    blur_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur_overlay.fill((0, 0, 0, 180))
    screen.blit(blur_overlay, (0, 0))

    prompt_text = font.render("Enter your name:", True, (255, 255, 0))
    name_text = font.render(player_name if player_name else "_", True, (255, 255, 255))
    hint_text = font.render("Press ENTER to confirm, ESC to cancel", True, (180, 180, 180))

    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 80))
    screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + 140))
    screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 200))