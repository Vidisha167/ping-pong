import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, paddles):
        """
        paddles: list of paddle objects (player, ai)
        """
        for paddle in paddles:
            next_rect = pygame.Rect(
                self.x + self.velocity_x,
                self.y + self.velocity_y,
                self.width,
                self.height
            )
            paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)

            if next_rect.colliderect(paddle_rect):
                self.velocity_x *= -1  # Reverse X direction

                # Optional: tweak Y velocity depending on collision point
                offset = (self.y + self.height / 2) - (paddle.y + paddle.height / 2)
                self.velocity_y = offset * 0.1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
