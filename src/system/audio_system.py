import pygame

def init_audio():
    pygame.mixer.init()
    pygame.mixer.music.load('src/assets/during game music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def play_move_sound():
    pygame.mixer.Sound('src/assets/carmoves.wav').play()

def play_dog_hit_sound():
    pygame.mixer.Sound('src/assets/dog.mp3').play()

def play_cat_hit_sound():
    pygame.mixer.Sound('src/assets/cat.mp3').play()

def play_bato_hit_sound():                                
    pygame.mixer.Sound('src/assets/bato.mp3').play()

def play_game_over_music():
    pygame.mixer.music.load('src/assets/weak.mp3')
    pygame.mixer.music.play(-1)

def stop_game_over_music():
    pygame.mixer.music.stop()

def play_in_game_music():
    pygame.mixer.music.load('src/assets/during game music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)