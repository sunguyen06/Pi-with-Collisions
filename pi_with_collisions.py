import pygame
import sys
from pygame.locals import *

# Set up the screen
pygame.init()
pygame.mixer.init()
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
clack = pygame.mixer.Sound("clack.wav")

# Create block class
class Block:
    def __init__(self, mass, pos, vel, color):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.color = color
        if self.mass >= 1 and self.mass < 40:
            self.size = 40
        elif self.mass >= 40:
            self.size = self.mass
        if self.size > 200:
            self.size = 200
    def render(self):
        pygame.draw.rect(screen, self.color, (self.pos, (screen_height/2) - self.size, self.size, self.size))

    def update(self, dt):
        self.pos += self.vel * dt

# Instantiate two blocks
b1Pos = 200  
b1Mass = 1

user_input = ''
user_prompt = True

# Beginning asking for user prompt
while user_prompt:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                user_prompt = False
        elif event.type == KEYUP:
            if event.key == K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

    # Visuals
    screen.fill((0, 0, 0))  # Set the background color to black
    font = pygame.font.Font(None, 30)
    text = font.render(f"Enter the mass of the moving block: {user_input}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.update()

# Update variables of the mass changed by the user
b2Mass = int(user_input)
print(f"Moving mass is {b2Mass}")
b2Pos = 300  
b2vel = -200000

block1 = Block(b1Mass, b1Pos, 0, (0, 0, 255))
block2 = Block(b2Mass, b2Pos, b2vel, (255, 0, 0))

# Main game loop
count = 0
dt = 0.001
running = True

# Add a horizontal line
line_y = screen_height // 2  # Adjust the y-coordinate of the line
line_color = (255, 255, 255)  # Set the color of the line to white

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update block positions
    block1.update(dt)
    block2.update(dt)

    # Check wall collision
    if block1.pos <= 0:
        clack.play()
        block1.pos = 0
        block1.vel *= -1
        count += 1

    # Check moving mass position, makes sure the moving mass never overlaps with the fixed mass
    if block2.pos <= 40:
        block2.pos = 41

    # Checks moving mass position to make sure it doesn't go off screen for improved visual clarity.
    if block2.pos + block2.size >= screen_width and abs(block1.vel) >= abs(block2.vel):
        block2.pos = screen_width - block2.size - 1

    # Check block collision
    if block1.pos + block1.size >= block2.pos:
        clack.play()
        block1.pos = block2.pos - block1.size

        m1 = block1.mass
        m2 = block2.mass
        v1i = block1.vel
        v2i = block2.vel

        mom1 = m1 * v1i + m2 * v2i

        v2f = (m1 * v2i - m1 * v1i - mom1) / (-1 * m2 - m1)
        v1f = v2i + v2f - v1i

        block1.vel = v1f
        block2.vel = v2f
        count += 1

    # Render the frame
    screen.fill((0, 0, 0))  # Set the background color to black
    font = pygame.font.Font(None, 30)
    text = font.render(f"Collisions: {count}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Display mass value
    text = font.render(f"M1: {b1Mass} kg   M2: {b2Mass} kg", True, (255, 255, 255))
    screen.blit(text, (10, (screen_height/2) + 30))  # Adjusted text position

    # Display velocity values
    vel_text = font.render(f"V1: {round(block1.vel/60, 2)} m/s   V2: {round(block2.vel/60, 2)} m/s", True, (255, 255, 255))
    screen.blit(vel_text, (10, (screen_height/2) + 80))  # Adjusted text position

    # Draw the horizontal line
    pygame.draw.line(screen, line_color, (0, line_y), (screen_width, line_y), 1)

    block1.render()
    block2.render()

    pygame.display.flip()
    clock.tick(60)