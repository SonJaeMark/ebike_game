import pygame
import random
from core.settings import WIDTH, HEIGHT, player_size, obstacle_y_pos, LANE_A_CENTERLINE, LANE_B_CENTERLINE, LANE_C_CENTERLINE, LANE_D_CENTERLINE, LANES, difficulty_speed_base
from entities.obstacles.obs import ObstaclesEnum

class Obstacles:
    IMAGE_PATHS = {
        ObstaclesEnum.CAT: 'src/assets/images/obstacle/cat.png',
        ObstaclesEnum.DOG: 'src/assets/images/obstacle/dog.png',
        ObstaclesEnum.BATO: 'src/assets/images/obstacle/bato.png'
    }

    def __init__(self):
        self.max_size = player_size  
        self.current_size = self.max_size // 2  # Initialize at half size immediately
        self.speed = difficulty_speed_base
        self.hidden_y = 0
        self.popup_timer = 0
        self.is_popped = False
        
        self.pos = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(0, 0)
        
        self.type = None
        self.master_image = None  
        self.image = None         
        self.reset()

    def reset(self):
        self.type = random.choice(list(ObstaclesEnum))
        self.current_size = self.max_size // 2  # Hard reset back to half size
        self.load_image() # This now safely creates a half-sized image instantly
        self.pick_lane_and_initialize()

    def pick_lane_and_initialize(self):
        lane = random.choice(LANES)
        start_point = lane[0]
        end_point = lane[1]

        if self.type != ObstaclesEnum.BATO:
            self.pos = pygame.math.Vector2(start_point.x - (self.current_size // 2), obstacle_y_pos)
            target_pos = pygame.math.Vector2(end_point.x - (self.max_size // 2), end_point.y)
            heading = target_pos - self.pos
            if heading.length() > 0:
                self.direction = heading.normalize()
            else:
                self.direction = pygame.math.Vector2(0, 1)
        else:
            lane_x = end_point.x - (self.current_size // 2)
            self.hidden_y = HEIGHT + 100
            self.pos = pygame.math.Vector2(lane_x, self.hidden_y)
            self.current_size = self.max_size        # ← full size immediately
            self.image = pygame.transform.smoothscale(self.master_image, (self.current_size, self.current_size))
            self.popup_timer = 0
            self.is_popped = False

    def update(self):
        if self.type != ObstaclesEnum.BATO:
            self.pos += self.direction * self.speed
            self.scale_obstacle()
            if self.pos.y > HEIGHT:
                self.reset()
        else:
            if not self.is_popped:
                self.pos.y -= 40
                if self.pos.y <= HEIGHT - 250:
                    self.is_popped = True
            else:
                if self.pos.y < 0:
                    self.reset()

    def load_image(self):
        image_path = self.IMAGE_PATHS.get(self.type)
        if image_path:
            if self.type == ObstaclesEnum.BATO:
                raw = pygame.image.load(image_path).convert_alpha()
                self.master_image = pygame.transform.scale(raw, (self.max_size, self.max_size))
            else:
                raw = pygame.image.load(image_path).convert_alpha()
                self.master_image = pygame.transform.scale(raw, (self.max_size, self.max_size))
        else:
            self.master_image = pygame.Surface((self.max_size, self.max_size))
            self.master_image.fill((255, 255, 255))
        
        self.image = pygame.transform.smoothscale(self.master_image, (self.current_size, self.current_size))
    
    def scale_obstacle(self):
        total_travel_y = HEIGHT - obstacle_y_pos
        current_travel_y = self.pos.y - obstacle_y_pos
        progress = max(0.0, min(1.0, current_travel_y / total_travel_y))
        
        start_scale = 0.5
        current_scale_factor = start_scale + (progress * (1.0 - start_scale))
        new_size = int(self.max_size * current_scale_factor)
        
        if new_size != self.current_size:
            old_center_x = self.pos.x + (self.current_size // 2)
            self.current_size = new_size
            self.image = pygame.transform.smoothscale(self.master_image, (self.current_size, self.current_size))
            self.pos.x = old_center_x - (self.current_size // 2)

    def update(self):
        
        if self.type !=ObstaclesEnum.BATO:
            self.pos += self.direction * self.speed
            self.scale_obstacle()

            if self.pos.y > HEIGHT:
                self.reset()

        else: 
            self.popup_timer += 1
            if not self.is_popped:
                self.pos.y -= 8

                if self.pos.y <= HEIGHT - 200:
                    self.is_popped = True   
                    self.popup_timer = 0

            else:
                if self.popup_timer > 90:  
                    self.pos.y += 8

                    if self.pos.y >= self.hidden_y:
                        self.reset()
    def draw(self, screen):
        self.update()
        screen.blit(self.image, (int(self.pos.x), int(self.pos.y)))

    @property
    def rect(self):
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.current_size, self.current_size)
