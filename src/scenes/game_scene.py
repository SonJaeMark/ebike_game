import pygame
from system.audio_system import play_move_sound, play_dog_hit_sound, play_cat_hit_sound
from entities.obstacles.obs import ObstaclesEnum

_score_saved = False

def save_score_once(score_system):
    global _score_saved
    if not _score_saved:
        score_system.save_to_leaderboard()
        _score_saved = True

def reset_save_flag():
    global _score_saved
    _score_saved = False

def in_game_scene(screen, clock, dt, ebike, obstacle, score_system, font, delarosa_img, LANES_TO_DRAW, WIDTH, HEIGHT):
    global road_offset
    if 'road_offset' not in globals():
        globals()['road_offset'] = 0.0

    road_speed = 4.0

    score_system.update(dt)
    globals()['road_offset'] += (road_speed * (dt / 1000.0))
    if globals()['road_offset'] >= 1.0:
        globals()['road_offset'] -= 1.0

    screen.fill((135, 206, 235))

    lane_colors = [(90, 90, 90), (95, 95, 95), (90, 90, 90), (95, 95, 95)]
    for i, lane_poly in enumerate(LANES_TO_DRAW):
        pygame.draw.polygon(screen, lane_colors[i], lane_poly)
        pygame.draw.polygon(screen, (120, 120, 120), lane_poly, 2)

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
    pygame.draw.polygon(screen, (126, 200, 80), left_border_poly)

    right_border_poly = [(LANES_TO_DRAW[3][1][0], HEIGHT), (WIDTH, HEIGHT), (WIDTH, 180), (LANES_TO_DRAW[3][2][0], 180)]
    pygame.draw.polygon(screen, (126, 200, 80), right_border_poly)

    old_y = obstacle.rect.y
    obstacle.draw(screen)

    if old_y <= HEIGHT and obstacle.rect.y < old_y:
        score_system.add_dodge_bonus()

    ebike.draw(screen)

    if ebike.is_colliding(obstacle):
        if obstacle.type == ObstaclesEnum.DOG:
            play_dog_hit_sound()
        elif obstacle.type == ObstaclesEnum.CAT:
            play_cat_hit_sound()
        obstacle.reset()
        return True
    return False

def pause_menu(screen, font, WIDTH, HEIGHT):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    pause_text = font.render("GAME PAUSED", True, (255, 255, 255))
    hint_text = font.render("Press SPACE to Resume", True, (200, 200, 200))

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 20))

def game_over(screen, font, score_system, WIDTH, HEIGHT):
    """Game Over terminal state rendering layout."""
    # Save score once — does NOT affect the screen rendering below
    save_score_once(score_system)

    screen.fill((20, 20, 20))

    game_over_text = font.render("GAME OVER", True, (255, 50, 50))
    score_msg = f"Final Score: {score_system.score}"
    score_text = font.render(score_msg, True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or ESC to Quit", True, (150, 150, 150))

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

def game_menu():
    pass

def leaderboard():
    pass