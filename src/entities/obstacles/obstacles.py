import pygame 
import random
from core.settings import WIDTH, HEIGHT, player_size, player_x, player_y, player_speed
from entities.obstacles.obs import ObstaclesEnum

class Obstacles:
    def __init__(self):
        self.x = player_x
        self.y = 0
        self.size = player_size
        self.image = None  
        self.speed = 3    

    def draw(self, screen, type):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH - self.size)
        
        match type:  
            case ObstaclesEnum.CAT:
                self.image = pygame.transform.scale(pygame.image.load('src/assets/cat.png').convert_alpha(), (self.size, self.size))
            case ObstaclesEnum.DOG:
                self.image = pygame.transform.scale(pygame.image.load('src/assets/dog.png').convert_alpha(), (self.size, self.size))
        
        screen.blit(self.image, (self.x, self.y)) 
    
    def randomize_x_position(self):
        self.x = random.randint(0, WIDTH - self.size)
        return self.x