import pygame
from core.settings import player_x, player_y, ebike_size

class Ebike:

    def __init__(self):

        # ================= PLAYER =================
        self.x = player_x
        self.y = player_y
        self.size = ebike_size

        # ================= LANES =================
        self.num_lanes = 4
        self.lane_width = 195

        self.road_x = (
            1280 - (self.num_lanes * self.lane_width)
        ) // 2

        self.lane_centers = []

        for i in range(self.num_lanes):

            center_x = (
                self.road_x +
                (i * self.lane_width) +
                (self.lane_width // 2)
            )

            self.lane_centers.append(center_x)

        self.current_lane = 1

        # SNAP TO CENTER
        self.x = (
            self.lane_centers[self.current_lane]
            - (self.size[0] // 2)
        )

        # ================= IMAGE =================
        self.image = pygame.image.load(
            'src/assets/images/vehicle/ebike.png' 
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            ebike_size
        )

    # ================= MOVE =================
    def move(self, event, play_move_sound):

        if event.type == pygame.KEYDOWN:

            # LEFT
            if event.key in (pygame.K_LEFT, pygame.K_a):

                if self.current_lane > 0:

                    self.current_lane -= 1
                    play_move_sound()

            # RIGHT
            if event.key in (pygame.K_RIGHT, pygame.K_d):

                if self.current_lane < self.num_lanes - 1:

                    self.current_lane += 1
                    play_move_sound()

            # UP
            if event.key in (pygame.K_UP, pygame.K_w):

                self.y -= 10

            # DOWN
            if event.key in (pygame.K_DOWN, pygame.K_s):

                self.y += 10

        # SNAP TO CENTER
        self.x = (
            self.lane_centers[self.current_lane]
            - (self.size[0] // 2)
        )
    # ================= DRAW =================
    def draw(self, screen):

        screen.blit(
            self.image,
            (self.x, self.y)
        )

    def is_colliding(self, obstacle_obj):
        ebike_rect = pygame.Rect(self.x, self.y, self.size[0] - 20 , self.size[1] - 20) 
        return ebike_rect.colliderect(obstacle_obj.rect)