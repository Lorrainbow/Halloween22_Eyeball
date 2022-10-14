# Simple pygame program
# Import and initialize the pygame library
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define the Iris object extending pygame.sprite.Sprite
class Iris(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Iris, self).__init__()
        self.surf = pygame.image.load("iris2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = pos

    # Move the sprite based on key presses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 30:
            self.rect.left = 30
        elif self.rect.right > EYEBALL_WIDTH-30:
            self.rect.right = EYEBALL_WIDTH-30
        if self.rect.top <= 30:
            self.rect.top = 30
        elif self.rect.bottom >= EYEBALL_HEIGHT-30:
            self.rect.bottom = EYEBALL_HEIGHT-30


class Eyeball(pygame.sprite.Sprite):
    def __init__(self, pos):
        global EYEBALL_WIDTH
        global EYEBALL_HEIGHT
        super(Eyeball, self).__init__()
        self.surf = pygame.image.load("eyeball_blank.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        EYEBALL_WIDTH = self.surf.get_width()
        EYEBALL_HEIGHT = self.surf.get_width()


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
iris = Iris((200, 200))
eyeball = Eyeball((100, 100))

# add eyeball
all_sprites = pygame.sprite.Group()
all_sprites.add(eyeball)
all_sprites.add(iris)

# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    iris.update(pressed_keys)

    # Fill the screen with sky blue
    screen.fill((0, 0, 0))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()