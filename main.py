import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display variables
window_width = 1500
window_height = 600
caption = "Car"
FPS = 60

# Create game window
gameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(caption)

# Set up clock for frame rate control
Clock = pygame.time.Clock()

class Car:
    def __init__(self, color: tuple[int], pos: list[int], size: int, speed: float = 1, friction: float = 0.9):
        """
        Initialize the car object.

        Args:
            color (tuple[int]): The RGB values for the car's color.
            pos (list[int]): The x and y coordinates of the car's position.
            size (int): The width and height of the car.
            speed (float, optional): The speed at which the car moves. Defaults to 1.
            friction (float, optional): The amount of friction that slows down the car. Defaults to 0.9.
        """
        self.color = color
        self.position = pos
        self.size = size
        self.velocity = [0, 0]
        self.friction = friction
        self.speed = speed

    def draw(self, screen: pygame.display):
        """Draw the car on the game window."""
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))

    def move(self) -> None:
        """
        Move the car based on user input and friction.

        The car's velocity is updated based on the user's key presses.
        The friction then slows down the car to its original speed over time.
        """
        keys = pygame.key.get_pressed()

        # Initialize direction vector
        dir = [0, 0]

        # Update direction based on user input
        if keys[pygame.K_w]:
            dir[1] -= self.speed
        if keys[pygame.K_s]:
            dir[1] += self.speed
        if keys[pygame.K_a]:
            dir[0] -= self.speed
        if keys[pygame.K_d]:
            dir[0] += self.speed

        # Normalize direction vector to ensure equal speed in all directions
        norm = math.sin(45) * self.speed
        if dir[0] != 0 and dir[1] != 0:
            if dir[0] > 0:
                dir[0] = norm
            elif dir[0] < 0:
                dir[0] = -norm

            if dir[1] > 0:
                dir[1] = norm
            elif dir[1] < 0:
                dir[1] = -norm

        # Update velocity and position
        self.velocity = [self.velocity[0] + dir[0], self.velocity[1] + dir[1]]
        self.position = [self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]]

        # Keep car within game window boundaries
        if self.position[0] > window_width - self.size:
            self.position[0] = window_width - self.size
        elif self.position[0] < 0:
            self.position[0] = 0

        if self.position[1] > window_height - self.size:
            self.position[1] = window_height - self.size
        elif self.position[1] < 0:
            self.position[1] = 0

        # Apply friction to slow down car over time
        self.velocity = [self.velocity[0] * self.friction, self.velocity[1] * self.friction]

# Create a new Car object
player = Car(color=(255, 0, 0), pos=(500, 500), size=50, speed=0.8)

# Game loop
Run = True
while Run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

    # Draw background and move player car
    gameDisplay.fill((0, 0, 0))
    player.move()
    player.draw(gameDisplay)

    # Update display
    pygame.display.update()

    # Cap frame rate
    Clock.tick(FPS)

# Quit Pygame
pygame.quit()