#! /usr/bin/python3

import pygame
import random
#import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Circle Attraction Simulation")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Circle properties
large_circle_radius = 100
center_position = pygame.Vector2(width // 2, height // 2)
small_circle_radius = 5
num_small_circles = 500
small_circles = []
eletstic_collision_coef = 0.9
earth_rotation_vel = 1.0
earth_friction_coef = 0.2

# Simulation parameters
gravity = 500.0


# Circle class
class Circle:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)

    def update_velocity(self):
        direction_to_center = center_position - self.position
        distance_to_center = direction_to_center.length()

        attraction_strength = gravity / (distance_to_center * distance_to_center)
        norm_direction = direction_to_center / distance_to_center
        self.velocity += norm_direction * attraction_strength
        self.position += self.velocity

    def set_velocity(self, newVel):
        self.velocity = newVel

    def check_collision(self, other):
        if other is self:
            # We cannot run into ourself
            return

        distance_vec = other.position - self.position 
        distance_length = distance_vec.length()
        if distance_length > self.radius + other.radius:
            # We have not collided.
            return

        # We have collided with another ball if we get here.
        # Calculate the velocity along distance_vec
        norm_dist_vec = distance_vec / distance_length

        my_speed_along_center_line = self.velocity.dot(norm_dist_vec)
        other_speed_along_center_line = other.velocity.dot(norm_dist_vec)

        diff_speed = my_speed_along_center_line - other_speed_along_center_line
        
        if diff_speed <= 0:
            # we are already moving apart
            return

        self.velocity = self.velocity + (eletstic_collision_coef * other_speed_along_center_line - my_speed_along_center_line) * norm_dist_vec
        other.set_velocity(other.velocity + (my_speed_along_center_line - eletstic_collision_coef * other_speed_along_center_line) * norm_dist_vec)

class BlueCircle(Circle):
    def set_velocity(self, newVel):
        pass

    def update_velocity(self):
        pass

    def check_collision(self, other):
        if other is self:
            return

        distance_vec = other.position - self.position 
        distance_length = distance_vec.length()
        if distance_length > self.radius + other.radius:
            # We have not collided.
            return

        norm_dist_vec = distance_vec / distance_length
        other_speed_along_center_line = other.velocity.dot(norm_dist_vec)
        if other_speed_along_center_line >= 0:
            # Moving away from the big planet.
            return

        perpend_vec = pygame.Vector2(-norm_dist_vec[1], norm_dist_vec[0])
        perpend_speed = other.velocity.dot(perpend_vec)

        speedChange = (earth_rotation_vel - perpend_speed) * earth_friction_coef
        change_in_perpend_vel = speedChange * perpend_vec
        
        # We have collided.
        norm_dist_vec = distance_vec / distance_length
        other_speed_along_center_line = other.velocity.dot(norm_dist_vec)
        other.set_velocity(other.velocity + change_in_perpend_vel - (1 + eletstic_collision_coef) * other_speed_along_center_line * norm_dist_vec)

# Create small circles with random starting positions
for _ in range(num_small_circles):
    x = random.randint(0, width)
    y = random.randint(0, height)
    small_circles.append(Circle(x, y, small_circle_radius))

large_circle = BlueCircle(center_position[0], center_position[1], large_circle_radius)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Update small circles' positions
    for circle in small_circles:
        large_circle.check_collision(circle)
        circle.update_velocity()

        # Check for collisions with other small circles
        for other_circle in small_circles:
            circle.check_collision(other_circle)

        large_circle.check_collision(circle)

    # Drawing
    screen.fill(BLACK)  # Clear screen
    pygame.draw.circle(screen, BLUE, center_position, large_circle_radius)  # Large circle
    for circle in small_circles:
        pygame.draw.circle(screen, RED, (int(circle.position[0]), int(circle.position[1])), circle.radius)  # Small circles

    pygame.display.flip()  # Update display
    pygame.time.delay(20)  # Control the frame rate

# Clean up
pygame.quit()
