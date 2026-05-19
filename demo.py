import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Box Collision System")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (30, 30, 45)
ARROW_COLOR = (242, 92, 84)     # Red
WASD_COLOR = (74, 153, 230)     # Blue
COLLIDE_COLOR = (244, 211, 94)  # Yellow
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.SysFont(None, 36)

# Box Setup (X, Y, Width, Height)
box_arrow = pygame.Rect(200, 250, 60, 60)
box_wasd = pygame.Rect(540, 250, 60, 60)

# Movement speed
SPEED = 5

# Game Loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Input Handling
    keys = pygame.key.get_pressed()

    # Arrow Keys Movement
    if keys[pygame.K_LEFT]:  box_arrow.x -= SPEED
    if keys[pygame.K_RIGHT]: box_arrow.x += SPEED
    if keys[pygame.K_UP]:    box_arrow.y -= SPEED
    if keys[pygame.K_DOWN]:  box_arrow.y += SPEED

    # WASD Keys Movement
    if keys[pygame.K_a]: box_wasd.x -= SPEED
    if keys[pygame.K_d]: box_wasd.x += SPEED
    if keys[pygame.K_w]: box_wasd.y -= SPEED
    if keys[pygame.K_s]: box_wasd.y += SPEED

    # 3. Screen Boundaries Check (Keep boxes on screen)
    box_arrow.clamp_ip(screen.get_rect())
    box_wasd.clamp_ip(screen.get_rect())

    # 4. Collision Detection
    is_colliding = box_arrow.colliderect(box_wasd)

    # 5. Drawing Updates
    screen.fill(BACKGROUND)

    # Set dynamic colors based on collision state
    color_arrow = COLLIDE_COLOR if is_colliding else ARROW_COLOR
    color_wasd = COLLIDE_COLOR if is_colliding else WASD_COLOR

    # Draw Boxes
    pygame.draw.rect(screen, color_arrow, box_arrow)
    pygame.draw.rect(screen, color_wasd, box_wasd)

    # Draw UI Text
    status_text = "COLLISION!" if is_colliding else "Move boxes into each other"
    text_surface = font.render(status_text, True, TEXT_COLOR)
    screen.blit(text_surface, (20, 20))

    # Refresh Screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
