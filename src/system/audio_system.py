import pygame

def init_audio():
    pygame.mixer.init()
    pygame.mixer.music.load('src/assets/during game music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


def play_move_sound():
    pygame.mixer.Sound('src/assets/carmoves.wav').play()