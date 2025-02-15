import pygame
import numpy as np
import random

class Ball:
    def __init__(self, position):
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array([random.randint(-5, 5), random.randint(-5, 5)], dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = 30

def check_ball_collision(ball1, ball2):
    # Distance between balls
    dist = np.linalg.norm(ball1.pos - ball2.pos)
    # Check if distance is less than the sum of their radii (collision condition)
    if dist < ball1.radius + ball2.radius:
        # Resolve the overlap
        overlap = ball1.radius + ball2.radius - dist
        direction = (ball1.pos - ball2.pos) / dist
        ball1.pos += direction * (overlap / 2)
        ball2.pos -= direction * (overlap / 2)
        
        # Update velocities based on elastic collision
        v1 = ball1.v - np.dot(ball1.v - ball2.v, direction) * direction
        v2 = ball2.v - np.dot(ball2.v - ball1.v, -direction) * -direction
        ball1.v, ball2.v = v1, v2

pygame.init()
width = 800
height = 800
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
circle_center = np.array([width / 2, height / 2], dtype=np.float64)
circle_radius = 300
ball_pos = np.array([width / 2, height / 2 - 120], dtype=np.float64)
balls = [Ball(ball_pos), Ball(ball_pos + np.array([100, 0])), Ball(ball_pos + np.array([50, 100]))]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i, ball in enumerate(balls):
        # Move the ball
        ball.pos += ball.v 
        # Check collision with circle boundary
        dist = np.linalg.norm(ball.pos - circle_center)
        if dist + ball.radius > circle_radius:
            d = ball.pos - circle_center
            d_unit = d / np.linalg.norm(d)
            ball.pos = circle_center + (circle_radius - ball.radius) * d_unit
            t = np.array([-d[1], d[0]], dtype=np.float64)
            proj_v_t = (np.dot(ball.v, t) / np.dot(t, t)) * t
            ball.v = 2 * proj_v_t - ball.v
            ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Check collision with other balls
        for j in range(i + 1, len(balls)):
            check_ball_collision(ball, balls[j])
    
    window.fill(black)
    # Draw connecting lines
    pygame.draw.line(window, white, balls[0].pos, balls[1].pos, 5)
    pygame.draw.line(window, white, balls[1].pos, balls[2].pos, 5)
    pygame.draw.line(window, white, balls[2].pos, balls[0].pos, 5)
    # Draw boundary circle
    pygame.draw.circle(window, white, circle_center.astype(int), circle_radius, 10)

    # Draw the balls
    for ball in balls:
        pygame.draw.circle(window, ball.color, ball.pos.astype(int), ball.radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
