import pygame
from core.settings import player_x, player_y, ebike_size

class Ebike:
    def __init__(self):
        self.x = player_x
        self.y = player_y
        self.size = ebike_size
        self.image = pygame.transform.scale(pygame.image.load('src/assets/ebike.png').convert_alpha(), ebike_size)

    def draw(self, screen, x,y):
        return screen.blit(self.image, (x, y))

    def is_colliding(self, obstacle_obj):
        ebike_rect = pygame.Rect(self.x, self.y, self.size[0] - 20 , self.size[1] - 20) 
        return ebike_rect.colliderect(obstacle_obj.rect)