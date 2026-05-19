import pygame
from system.audio_system import init_audio, play_move_sound
from core.settings import WIDTH, HEIGHT, FPS, player_size, player_x, player_y, player_speed
from entities.ebike import Ebike

pygame.init()
init_audio()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Project")

clock = pygame.time.Clock()

running = True

# player_img = pygame.image.load('src/assets/dog.png').convert_alpha()
# player_img = pygame.transform.scale(pygame.image.load('src/assets/dog.png').convert_alpha(), (player_size, player_size))
cat_img = pygame.transform.scale(pygame.image.load('src/assets/cat.png').convert_alpha(), (player_size, player_size))

ebike = Ebike()

try:
    # player_img = pygame.transform.scale(player_img, (player_size, player_size))
    cat_img = pygame.transform.scale(cat_img, (player_size, player_size))
except Exception as e:
    print(f"Error loading images: {e}")
    # player_img = pygame.Surface((player_size, player_size))
    # player_img.fill((255, 0, 0))
    cat_img = pygame.Surface((player_size, player_size))
    cat_img.fill((0, 0, 255))

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
        play_move_sound()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
        play_move_sound()

    # ================= DRAW =================
    screen.fill((30, 30, 30))

    # Draw player image
    # screen.blit(player_img, (player_x, player_y))
    ebike.draw(screen, player_x, player_y)

    # Draw cat image
    screen.blit(cat_img, (player_x + 100, player_y))

    pygame.display.flip()

pygame.quit()