import pygame
from core.settings import player_x, player_y, ebike_size
# Import your road polygon coordinate configurations
from core.settings import ROAD_A, ROAD_B, ROAD_C, ROAD_D

class Ebike:

    def __init__(self):
        # ================= PLAYER POSITION =================
        self.y = player_y
        self.size = ebike_size  # (width, height) tuple
        self.current_lane = 1   # Start lane index (0 to 3)

        # ================= PERSPECTIVE LANES CONFIG =================
        # Extract the Top and Bottom segments from your global road polygons.
        # ROAD formats: (Bottom-Left, Bottom-Right, Top-Right, Top-Left)
        # Top segment lane center x = average of Top-Left and Top-Right x values at Y=180
        # Bottom segment lane center x = average of Bottom-Left and Bottom-Right x values at Y=HEIGHT (mapped from 0)
        
        # We manually map out the precise center tracks for both Horizon (top) and Foreground (bottom)
        # Note: Your road configurations use Y=0 for bottom, which maps to screen HEIGHT (e.g. 600 or 720)
        screen_height = 600 # Fallback/Adjust based on your game's actual window height
        
        self.top_centers = [
            (ROAD_A[3][0] + ROAD_A[2][0]) / 2, # Lane A Center at Horizon (Y=180)
            (ROAD_B[3][0] + ROAD_B[2][0]) / 2, # Lane B Center at Horizon (Y=180)
            (ROAD_C[3][0] + ROAD_C[2][0]) / 2, # Lane C Center at Horizon (Y=180)
            (ROAD_D[3][0] + ROAD_D[2][0]) / 2, # Lane D Center at Horizon (Y=180)
        ]
        
        self.bottom_centers = [
            (ROAD_A[0][0] + ROAD_A[1][0]) / 2 , # Lane A Center at Foreground
            (ROAD_B[0][0] + ROAD_B[1][0]) / 2, # Lane B Center at Foreground
            (ROAD_C[0][0] + ROAD_C[1][0]) / 2, # Lane C Center at Foreground
            (ROAD_D[0][0] + ROAD_D[1][0]) / 2, # Lane D Center at Foreground
        ]

        self.top_y = 180.0
        self.bottom_y = float(screen_height)

        # Initial Snap calculation
        self.x = 0
        self.snap_to_perspective_lane()

        # ================= IMAGE ASSET =================
        self.image = pygame.image.load(
            'src/assets/images/vehicle/ebike.png' 
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            ebike_size
        )

    def snap_to_perspective_lane(self):
        """Calculates exact perspective X position matching the current Y value."""
        # 1. Determine relative vertical placement scale between horizon limits
        total_travel_y = self.bottom_y - self.top_y
        current_travel_y = self.y - self.top_y
        progress = max(0.0, min(1.0, current_travel_y / total_travel_y))

        # 2. Grab center limits for currently selected tracking track
        start_x = self.top_centers[self.current_lane]
        end_x = self.bottom_centers[self.current_lane]

        # 3. Linearly interpolate actual tracking value based on current height progress
        lane_center_x = start_x + (progress * (end_x - start_x))

        # 4. Center-align bounding anchor width offset targets
        self.x = lane_center_x - (self.size[0] // 2)

    # ================= ACTION CONTROL LAYER =================
    def move(self, event, play_move_sound):
        if event.type == pygame.KEYDOWN:
            # SHIFT LEFT
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.current_lane > 0:
                    self.current_lane -= 1
                    play_move_sound()

            # SHIFT RIGHT
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.current_lane < len(self.top_centers) - 1:
                    self.current_lane += 1
                    play_move_sound()

            # ADVANCE/UP (Closer to Horizon)
            if event.key in (pygame.K_UP, pygame.K_w):
                # Clamp boundary so bike can't travel completely beyond horizon limit line
                if self.y > self.top_y + 20:
                    self.y -= 10

            # FALLBACK/DOWN (Closer to Foreground)
            if event.key in (pygame.K_DOWN, pygame.K_s):
                if self.y < self.bottom_y - self.size[1]:
                    self.y += 10

        # Enforce structural tracking calculation adjustments whenever position values evolve
        self.snap_to_perspective_lane()

    # ================= RENDERING AND COLLISION =================
    def draw(self, screen):
        # Dynamically scale ebike asset if you want it to shrink near the horizon lines
        # For now, just render normally at calculated snap anchors
        screen.blit(self.image, (int(self.x), int(self.y)))

    def is_colliding(self, obstacle_obj):
        # Margins adjusted dynamically matching vector rect constraints safely
        ebike_rect = pygame.Rect(int(self.x) + 10, int(self.y) + 10, self.size[0] - 20 , self.size[1] - 20) 
        return ebike_rect.colliderect(obstacle_obj.rect)
