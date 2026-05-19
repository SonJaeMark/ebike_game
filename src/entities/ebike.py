import pygame
from core.settings import player_x, player_y, player_size

class Ebike:
    def __init__(self):
        self.x = player_x
        self.y = player_y
        self.size = player_size
        self.image = pygame.transform.scale(pygame.image.load('src/assets/dog.png').convert_alpha(), (player_size, player_size))

    def draw(self, screen, x,y):
        return screen.blit(self.image, (x, y))