import pygame
from core.settings import player_y, ebike_size
from core.settings import ROAD_A, ROAD_B, ROAD_C, ROAD_D, HEIGHT


class Ebike:

    def __init__(self):
        self.y = player_y
        self.size = ebike_size
        
        self.current_lane = 1.0
        self.target_lane = 1.0
        self.lane_speed = 0.09   

    
        self.moving_left = False
        self.moving_right = False

        self.top_centers = [
            (ROAD_A[3][0] + ROAD_A[2][0]) / 2,
            (ROAD_B[3][0] + ROAD_B[2][0]) / 2,
            (ROAD_C[3][0] + ROAD_C[2][0]) / 2,
            (ROAD_D[3][0] + ROAD_D[2][0]) / 2,
        ]

        self.bottom_centers = [
            (ROAD_A[0][0] + ROAD_A[1][0]) / 2 - 100,
            (ROAD_B[0][0] + ROAD_B[1][0]) / 2 - 20,
            (ROAD_C[0][0] + ROAD_C[1][0]) / 2 + 20,
            (ROAD_D[0][0] + ROAD_D[1][0]) / 2 + 90,
        ]

        self.top_y = 180.0
        self.bottom_y = float(HEIGHT)

        self.x = 0
        self.snap_to_perspective_lane()

        self.image = pygame.image.load(
            'src/assets/images/vehicle/ebike.png'
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, ebike_size)

    def update_lane(self):
        diff = self.target_lane - self.current_lane
        if abs(diff) > 0.001:
            self.current_lane += diff * self.lane_speed
        else:
            self.current_lane = self.target_lane

    def snap_to_perspective_lane(self):
        lane = self.current_lane
        lane_left = int(lane)
        lane_right = min(lane_left + 1, len(self.top_centers) - 1)
        t = lane - lane_left

        top_x = self.top_centers[lane_left] * (1 - t) + self.top_centers[lane_right] * t
        bottom_x = self.bottom_centers[lane_left] * (1 - t) + self.bottom_centers[lane_right] * t

        total_travel_y = self.bottom_y - self.top_y
        current_travel_y = self.y - self.top_y
        progress = max(0.0, min(1.0, current_travel_y / total_travel_y))

        lane_center_x = top_x + (progress * (bottom_x - top_x))
        self.x = lane_center_x - (self.size[0] // 2)

    def handle_input(self, play_move_sound):
        """Single lane change per key press + smooth animation"""
        keys = pygame.key.get_pressed()
        moved = False

        # LEFT movement (A or Left Arrow)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.target_lane > 0:
            if not self.moving_left:           # Only move if key was just pressed
                self.target_lane -= 1
                moved = True
                self.moving_left = True

        # RIGHT movement (D or Right Arrow)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.target_lane < len(self.top_centers) - 1:
            if not self.moving_right:          # Only move if key was just pressed
                self.target_lane += 1
                moved = True
                self.moving_right = True

        if moved:
            play_move_sound()

        if not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.moving_left = False

        if not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.moving_right = False

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.y > self.top_y + 20:
                self.y -= 8
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.y < self.bottom_y - self.size[1]:
                self.y += 8

    def update(self):
        self.update_lane()
        self.snap_to_perspective_lane()

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

    def is_colliding(self, obstacle_obj):
        ebike_rect = pygame.Rect(int(self.x) + 10, int(self.y) + 10, 
                                self.size[0] - 20, self.size[1] - 20)
        return ebike_rect.colliderect(obstacle_obj.rect)