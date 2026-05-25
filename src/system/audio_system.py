import pygame

_current_music = None

def init_audio():
    pygame.mixer.init()
    global _current_music
    _current_music = None

def play_move_sound():
    pygame.mixer.Sound('src/assets/carmoves.wav').play()

def play_dog_hit_sound():
    pygame.mixer.Sound('src/assets/dog.mp3').play()

def play_cat_hit_sound():
    pygame.mixer.Sound('src/assets/cat.mp3').play()

def play_bato_hit_sound():                                
    pygame.mixer.Sound('src/assets/bato.mp3').play()

def play_game_over_music():
    global _current_music
    if _current_music != 'game_over':
        pygame.mixer.music.load('src/assets/weak.mp3')
        pygame.mixer.music.play(-1)
        _current_music = 'game_over'

def stop_game_over_music():
    pygame.mixer.music.stop()
    global _current_music
    _current_music = None

def play_in_game_music():
    global _current_music
    if _current_music != 'during_game':
        pygame.mixer.music.load('src/assets/during game music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        _current_music = 'during_game'

def restart_in_game_music():
    global _current_music
    pygame.mixer.music.load('src/assets/during game music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    _current_music = 'during_game'