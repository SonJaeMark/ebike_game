import pygame
import random
from core.settings import WIDTH, HEIGHT, player_size, LANE_CENTERS, obstacle_y_pos
from entities.obstacles.obs import ObstaclesEnum

class Obstacles:
    IMAGE_PATHS = {
        ObstaclesEnum.CAT: 'src/assets/cat.png',
        ObstaclesEnum.DOG: 'src/assets/dog.png',
    }

    def __init__(self):
        self.size = player_size
        self.speed = 6
        self.x = 0
        self.y = -self.size
        self.type = None
        self.image = None
        self.reset()

    def reset(self):
        self.y = -self.size
        self.type = random.choice(list(ObstaclesEnum))
        self.randomize_x_position()
        self.load_image()

    def load_image(self):
        image_path = self.IMAGE_PATHS.get(self.type)
        if image_path:
            self.image = pygame.transform.scale(
                pygame.image.load(image_path).convert_alpha(),
                (self.size, self.size)
            )
        else:
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((255, 255, 255))

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()

    def draw(self, screen):
        self.update()
        screen.blit(self.image, (self.x, self.y))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def randomize_x_position(self):
        lane_center = random.choice(LANE_CENTERS)
        self.x = lane_center - (self.size // 2)
        return self.x