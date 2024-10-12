import pygame
import numpy as np
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Ball Simulator with Walls")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Red = (255, 0, 0)

# Physics constants
GRAVITY = np.array([0, 0.5])

# Load and scale wall image
wall_image_path = os.path.join('assets', 'wall_image.png')
wall_image = pygame.image.load(wall_image_path).convert_alpha()
wall_image = pygame.transform.scale(wall_image, (WIDTH, HEIGHT))

class PhysicsObject:
    def __init__(self, position, velocity, mass, shape):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.shape = shape

    def update(self):
        self.velocity += GRAVITY
        self.position += self.velocity

    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, Red, self.position.astype(int), 20)

class Ball(PhysicsObject):
    def __init__(self, position, velocity, mass):
        super().__init__(position, velocity, mass, 'circle')

    def update(self, wall_image, balls):
        super().update()
        self.check_collision(wall_image)
        if self.position[1] > HEIGHT or self.position[0] < 0 or self.position[0] > WIDTH:  # If ball goes off the screen, remove it
            balls.remove(self)


    def check_collision(self, wall_image):
        

class Wall:
    def __init__(self, image):
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

def main():
    clock = pygame.time.Clock()
    balls = []
    wall = Wall(wall_image)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Spacebar to shoot ball
                    mouse_pos = pygame.mouse.get_pos()
                    pos = np.array([mouse_pos[0], mouse_pos[1]])  # Shoot from the center
                    # direction = np.arctan2(mouse_pos[1] - pos[1], mouse_pos[0] - pos[0])
                    # dx, dy = 10 * np.cos(direction), 10 * np.sin(direction)
                    velocity = np.array([0,0])  # Example initial velocity
                    balls.append(Ball(pos, velocity, 1))
                elif event.key == pygame.K_c:  # Clear all balls
                    balls = []

        screen.fill(WHITE)
        wall.draw(screen)
        for ball in balls:
            ball.update(wall.image, balls)
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
