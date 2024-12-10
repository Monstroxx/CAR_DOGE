import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Analog Clock")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Define clock parameters
radius = width // 2 - 10
center_x, center_y = width // 2, height // 2

def draw_hand(surface, angle, length, color):
    x = center_x + int(math.sin(angle) * length)
    y = center_y - int(math.cos(angle) * length)
    pygame.draw.line(surface, color, (center_x, center_y), (x, y), 5)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current time
    current_time = pygame.time.get_ticks()
    seconds = current_time // 1000 % 60
    minutes = (current_time // (1000 * 60)) % 60
    hours = (current_time // (1000 * 60 * 60)) % 12

    # Calculate angles for hour, minute and second hands
    sec_angle = seconds / 60 * math.pi * 2 - math.pi / 2
    min_angle = minutes / 60 * math.pi * 2 + sec_angle / 60 - math.pi / 2
    hour_angle = hours / 12 * math.pi * 2 + min_angle / 12 - math.pi / 2

    # Draw the clock face
    screen.fill(white)
    pygame.draw.circle(screen, black, (center_x, center_y), radius, 5)

    # Draw numbers on the clock
    for i in range(1, 13):
        angle = math.radians(i * 30 - 90)
        x = center_x + int(math.sin(angle) * (radius - 20))
        y = center_y - int(math.cos(angle) * (radius - 20))
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(i), True, black)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    # Draw hands
    draw_hand(screen, sec_angle, radius - 10, red)  # Second hand in red
    draw_hand(screen, min_angle, radius - 30, black)  # Minute hand
    draw_hand(screen, hour_angle, radius // 2, black)  # Hour hand

    pygame.display.flip()

# Quit Pygame
pygame.quit()

