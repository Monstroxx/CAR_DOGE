import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up display variables
window_width = 1500
window_height = 600
caption = "Car"
FPS = 60

control1 = {
    "w": pygame.K_w,
    "a": pygame.K_a,
    "s": pygame.K_s,
    "d": pygame.K_d,
}

control2 = {
    "w": pygame.K_UP,
    "a": pygame.K_LEFT,
    "s": pygame.K_DOWN,
    "d": pygame.K_RIGHT,
}

skins = {
    'Car': "CAR_DOGE/Car.png",
    'Audi': "CAR_DOGE/Audi.png",
    'Ambulance': "CAR_DOGE/Ambulance.png",
    'Mini_truck': "CAR_DOGE/Mini_truck.png",
    'taxi': "CAR_DOGE/taxi.png",
    'truck': "CAR_DOGE/truck.png",
    'Minni_van': "CAR_DOGE/Minni_van.png",
    'Black_viper': "CAR_DOGE/Black_viper.png",
}

# Create game window
gameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(caption)

# Set up clock for frame rate control
Clock = pygame.time.Clock()

class Car:
    def __init__(self, texture: str, pos: list[int], size: int, speed: float = 1, friction: float = 0.9):
        """
        Initialize the car object.

        Args:
            color (tuple[int]): The RGB values for the car's color.
            pos (list[int]): The x and y coordinates of the car's position.
            size (int): The width and height of the car.
            speed (float, optional): The speed at which the car moves. Defaults to 1.
            friction (float, optional): The amount of friction that slows down the car. Defaults to 0.9.
        """
        self.Texture = pygame.image.load(texture)
        self.Texture = pygame.transform.scale(self.Texture, (size, size))

        self.TextureRot = pygame.transform.rotate(self.Texture, 180)


        self.position = pos
        self.size = size
        self.velocity = [0, 0]
        self.friction = friction
        self.speed = speed

    def draw(self, screen: pygame.display):
        #Draw the car on the game window.
        pygame.draw.rect(screen, (0,0,0), (self.position[0], self.position[1], self.size, self.size))
        gameDisplay.blit(self.Texture, (self.position[0], self.position[1]))

    def move(self, KeyUp: int, KeyDown: int, Keyleft: int, KeyRight: int, minPos: list[int], maxPos: list[int]):
        """
        Move the car based on user input and friction.
        The car's velocity is updated based on the user's key presses.
        The friction then slows down the car to its original speed over time.
        """
        keys = pygame.key.get_pressed()

        # Initialize direction vector
        dir = [0, 0]

        # Update direction based on user input
        if keys[KeyUp]:
            dir[1] -= self.speed
            self.Texture = pygame.transform.rotate(self.TextureRot, 180)
        if keys[KeyDown]:
            dir[1] += self.speed
            self.Texture = pygame.transform.rotate(self.TextureRot, -360)
        if keys[Keyleft]:
            dir[0] -= self.speed
            self.Texture = pygame.transform.rotate(self.TextureRot, -90)
        if keys[KeyRight]:
            dir[0] += self.speed
            self.Texture = pygame.transform.rotate(self.TextureRot, 90)

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
        if self.position[0] > maxPos[0] - self.size:
            self.position[0] = maxPos[0] - self.size
        elif self.position[0] < minPos[0]:
            self.position[0] = minPos[0]

        if self.position[1] > maxPos[1] - self.size:
            self.position[1] = maxPos[1] - self.size
        elif self.position[1] < minPos[1]:
            self.position[1] = minPos[1]

        # Apply friction to slow down car over time
        self.velocity = [self.velocity[0] * self.friction, self.velocity[1] * self.friction]

class NPC:
    def __init__(self, size: int):

        self.position : list[int] = [0, 0]
        self.size = size

        self.spawn()

    def draw(self, screen: pygame.display):
        #Draw the car on the game window.
        pygame.draw.rect(screen, (0,0,0), (self.position[0], self.position[1], self.size, self.size))
        gameDisplay.blit(self.Texture, (self.position[0], self.position[1]))
    
    def spawn(self):
        #Spawn car npc at start
        self.direction = int(random.choice([-1, 1])) #-1 for left
        self.ran_start = random.randint(0, window_height - self.size)
        
        self.position[1] = self.ran_start
        if self.direction == 1:
            self.position[0] = 0
        elif self.direction == -1:
            self.position[0] = window_width -self.size
        
        self.speed: float = 1
        self.speed = random.randint(4, 12)

        texture_list = [skins["Car"], skins["Audi"], skins["Ambulance"], skins["Mini_truck"], skins["taxi"], skins["truck"], skins["Black_viper"]]#, skins["Minni_van"]

        self.Texture = random.choice(texture_list)
        self.Texture = pygame.image.load(self.Texture)
        self.Texture = pygame.transform.scale(self.Texture, (self.size, self.size))
        self.TextureRot = pygame.transform.rotate(self.Texture, 180)
        if self.direction == 1:
            self.Texture = pygame.transform.rotate(self.TextureRot, 90)
        if self.direction == -1:
            self.Texture = pygame.transform.rotate(self.TextureRot, -90)
        self.TextureRot = pygame.transform.rotate(self.Texture, 180)

    def move(self):
        #move car npc from start to end
        self.position[0] += self.speed * self.direction

        if self.position[0] > window_width + self.size or self.position[0] < 0 -self.size:
            self.spawn()


# Create a new Car object
player = Car(texture=skins['Car'], pos=(500, 500), size=50, speed=0.8)
player2 = Car(texture=skins['Audi'], pos=(1000, 500), size=50, speed=0.8)


NPC1 = NPC(size=50)
NPC2 = NPC(size=50)
# Game loop
Run = True
while Run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

    # Draw background and move player car
    gameDisplay.fill((0, 0, 0))
    player.move(control1["w"], control1["s"], control1["a"], control1["d"],[0,0],[window_width,window_height])
    player2.move(control2["w"], control2["s"], control2["a"], control2["d"],[0,0],[window_width,window_height])
    player.draw(gameDisplay)
    player2.draw(gameDisplay)

    NPC1.move()
    NPC1.draw(gameDisplay)
    NPC2.move()
    NPC2.draw(gameDisplay)

    # Update display
    pygame.display.update()

    # Cap frame rate
    Clock.tick(FPS)

# Quit Pygame
pygame.quit()