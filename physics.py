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
        ball_radius = 20
        probe_distance = 10

        def check_pixel_collision(x, y):
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                return wall_image.get_at((x, y)) != WHITE
            return False

        def find_collision_direction(ball_dir,dire = 0):
            for distance in range(1, probe_distance + 1):
                angleset = ball_dir
                for angle in range(ball_dir, ball_dir+360, 5):
                    rad = np.radians(ball_dir + angleset)
                    check_x = int(self.position[0] + (distance * np.cos(rad)))
                    check_y = int(self.position[1] + (distance * np.sin(rad)))
                    if check_pixel_collision(check_x, check_y):
                        return np.array([np.cos(rad), np.sin(rad)])
                    angleset += dire
            return None

        def check_main_ball_collision():
            for distance in range(1, ball_radius + 1):
                for angle in range(0, 360, 5):  # Check every 5 degrees
                    rad = np.radians(angle)
                    check_x = int(self.position[0] + (distance * np.cos(rad)))
                    check_y = int(self.position[1] + (distance * np.sin(rad)))
                    if check_pixel_collision(check_x, check_y):
                        return True
            return False

        # Check for main ball collision
        if check_main_ball_collision():
            ball_dir = np.arctan2(self.velocity[1], self.velocity[0])
            ball_dir = np.degrees(ball_dir)
            ball_dir = int(ball_dir)
            dir_start = find_collision_direction(ball_dir,-5)  # Find start direction
            dir_end = find_collision_direction(ball_dir,5)  # Find end direction

            if dir_start is not None and dir_end is not None:
                normal = (dir_start + dir_end) / 2
                self.velocity -= 2 * np.dot(self.velocity, normal) * normal
                overlap = ball_radius - np.linalg.norm(self.position - (self.position + normal * ball_radius))
                self.position += normal * overlap

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
                    pos = np.array([WIDTH // 2, HEIGHT // 3])  # Shoot from the center
                    mouse_pos = np.array(pygame.mouse.get_pos())
                    direction = np.arctan2(mouse_pos[1] - pos[1], mouse_pos[0] - pos[0])
                    dx, dy = 10 * np.cos(direction), 10 * np.sin(direction)
                    velocity = np.array([dx,dy])  # Example initial velocity
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