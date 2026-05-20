import pygame
import sys

# 1. Setup Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Diagonal Path Movement")
clock = pygame.time.Clock()

# 2. Define Diagonal Path (Zigzag pattern)
path = [(50, 50), (350, 550), (450, 50), (750, 550), (750, 50), (50, 550)]
target_idx = 0

# 3. Define Moving Object
box_size = 40
box_pos = pygame.math.Vector2(path[0])  # Start at first waypoint
speed = 6

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Game Logic: Vector Movement (Handles Diagonals Automatically) ---
    target = pygame.math.Vector2(path[target_idx])
    direction = target - box_pos
    distance = direction.length()

    if distance <= speed:
        box_pos = target
        target_idx = (target_idx + 1) % len(path)
    else:
        # Normalizing ensures speed remains constant on diagonals
        direction.normalize_ip()
        box_pos += direction * speed

    # --- Drawing ---
    screen.fill((30, 30, 30))

    # Draw the path
    pygame.draw.lines(screen, (100, 100, 100), True, path, 2)
    for pt in path:
        pygame.draw.circle(screen, (255, 0, 0), pt, 6)

    # Draw the box
    box_rect = pygame.Rect(0, 0, box_size, box_size)
    box_rect.center = (int(box_pos.x), int(box_pos.y))
    pygame.draw.rect(screen, (0, 150, 255), box_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
