import pygame
from system.audio_system import init_audio, play_move_sound
from entities.ebike import Ebike
from entities.obstacles.obstacles import Obstacles
from entities.obstacles.obs import ObstaclesEnum  
from core.settings import WIDTH, HEIGHT, FPS, player_size, player_x, player_y, player_speed, ebike_size, obstacle_y_pos
pygame.init()
init_audio()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E-Bike Game")

clock = pygame.time.Clock()

# ================= ROAD SETTINGS =================
BORDER_WIDTH = 250

NUM_LANES = 4
LANE_WIDTH = 195
LANE_PADDING = 10

ROAD_WIDTH = NUM_LANES * LANE_WIDTH
ROAD_X = (WIDTH - ROAD_WIDTH) // 2

# ================= PLAYER SETTINGS =================
PLAYER_SIZE = 128

# ================= LOAD OBJECTS =================
ebike = Ebike()
obstacle = Obstacles()

# ================= LOAD IMAGES =================
try:

    cat_img = pygame.image.load(
        "src/assets/cat.png"
    ).convert_alpha()

    cat_img = pygame.transform.scale(
        cat_img,
        (PLAYER_SIZE, PLAYER_SIZE)
    )

except Exception as e:

    print("Image loading error:", e)

    cat_img = pygame.Surface(
        (PLAYER_SIZE, PLAYER_SIZE)
    )

    cat_img.fill((0, 0, 255))

# ================= GAME LOOP =================
running = True

while running:

    dt = clock.tick(FPS)

    # ================= EVENTS =================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        ebike.move(event, play_move_sound)

    # ================= DRAW =================
    screen.fill((60, 60, 60))

    # LEFT BORDER
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (0, 0, BORDER_WIDTH, HEIGHT)
    )
    # RIGHT BORDER
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (
            WIDTH - BORDER_WIDTH,
            0,
            BORDER_WIDTH,
            HEIGHT
        )
    )

    # ROAD
    pygame.draw.rect(
        screen,
        (90, 90, 90),
        (
            ROAD_X,
            0,
            ROAD_WIDTH,
            HEIGHT
        )
    )

    # LANE LINES
    for i in range(1, NUM_LANES):

        x = ROAD_X + (i * LANE_WIDTH)

        pygame.draw.line(
            screen,
            (255, 255, 0),
            (x, 0),
            (x, HEIGHT),
            4
        )

    # LANE PADDING VISUAL
    for i in range(NUM_LANES):

        lane_x = ROAD_X + (i * LANE_WIDTH)

        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (
                lane_x + LANE_PADDING,
                0,
                LANE_WIDTH - (LANE_PADDING * 2),
                HEIGHT
            ),
            1
        )

    
    # DRAW RANDOM OBSTACLE
    obstacle.draw(screen)

    # DRAW EBIKE
    ebike.draw(screen)

    pygame.display.flip()

pygame.quit()