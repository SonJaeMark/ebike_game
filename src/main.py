import pygame
from core.settings import WIDTH, HEIGHT, FPS, player_size, player_x, player_y, player_speed

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Project")

clock = pygame.time.Clock()

running = True

# player_img = pygame.image.load('src/assets/dog.png').convert_alpha()
player_img = pygame.transform.scale(pygame.image.load('src/assets/dog.png').convert_alpha(), (64, 64))


while running:
    dt = clock.tick(FPS)

    # ================= EVENTS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ================= MOVEMENT =================
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed

    # ================= DRAW =================
    screen.fill((30, 30, 30))

    # Draw player image
    screen.blit(player_img, (player_x, player_y))

    pygame.display.flip()

pygame.quit()