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
import time

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
blinking = -1

# Define the Iris object extending pygame.sprite.Sprite
class Iris(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Iris, self).__init__()
        self.surf = pygame.image.load("iris2.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = pos

    # Move the sprite based on key presses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            print("UP")
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            print("DOWN")
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            print("LEFT")
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            print("RIGHT")
            self.rect.move_ip(5, 0)

        # print(self.rect.left)
        # print(self.rect.right)
        # Keep player on the screen
        if self.rect.left < 30:
            self.rect.left = 30
        elif self.rect.right > EYEBALL_WIDTH-30:
            self.rect.right = EYEBALL_WIDTH-30
        if self.rect.top <= 30:
            self.rect.top = 30
        elif self.rect.bottom >= EYEBALL_HEIGHT-30:
            self.rect.bottom = EYEBALL_HEIGHT-30


class Eyelid(pygame.sprite.Sprite):
    def __init__(self):
        super(Eyelid, self).__init__()

        self.images = []
        self.images.append(pygame.image.load("eyelid1.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid2.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid3.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid4.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid5.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid6.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid7.png").convert_alpha())
        self.images.append(pygame.image.load("eyelid8.png").convert_alpha())

        self.surf = self.images[0]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.blinking = -1
        self.last_blink = 0

    # blink when i press up
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
           self.blinking = 0
           self.last_blink = time.time()

        if self.blinking >= 0:
            if self.blinking < len(self.images):
                self.surf = self.images[self.blinking]
            elif self.blinking >= len(self.images):
                self.surf = self.images[len(self.images) * 2 - self.blinking - 1]

            if time.time() - self.last_blink > 0.1:
                self.last_blink = time.time()
                self.blinking += 1
            if self.blinking >= len(self.images) * 2:
                self.blinking = -1
                self.surf = self.images[0]


class Eyeball(pygame.sprite.Sprite):
    def __init__(self):
        global EYEBALL_WIDTH
        global EYEBALL_HEIGHT
        super(Eyeball, self).__init__()

        self.surf = pygame.image.load("eyeball_blank.png").convert_alpha()
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
eyelid = Eyelid()
iris = Iris((200, 200))
eyeball = Eyeball()

# add eyeball
all_sprites = pygame.sprite.Group()

# add the sprites in order
all_sprites.add(eyeball)
all_sprites.add(iris)
all_sprites.add(eyelid)


running = True
while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # stop on ESC
            if event.key == K_ESCAPE:
                running = False
        # stop on quit
        elif event.type == QUIT:
            running = False

    # what was pressed?
    pressed_keys = pygame.key.get_pressed()

    # update the iris and the eyelid
    iris.update(pressed_keys)
    eyelid.update(pressed_keys)


    screen.fill((255, 255, 255))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip everything to the display
    pygame.display.flip()

    # 30fps
    clock.tick(30)