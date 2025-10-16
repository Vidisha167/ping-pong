import pygame
import random

# --- Ball class ---
class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, paddle_sound):
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
        self.paddle_sound = paddle_sound

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, paddles):
        for paddle in paddles:
            next_rect = pygame.Rect(
                self.x + self.velocity_x,
                self.y + self.velocity_y,
                self.width,
                self.height
            )
            paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            if next_rect.colliderect(paddle_rect):
                self.velocity_x *= -1
                # Play paddle hit sound safely
                if self.paddle_sound:
                    self.paddle_sound.play()
                # Adjust Y velocity based on collision point
                offset = (self.y + self.height / 2) - (paddle.y + paddle.height / 2)
                self.velocity_y = offset * 0.1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Paddle class ---
class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, dy):
        self.y += dy
        # Keep paddle inside screen
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > 600:  # assuming screen height
            self.y = 600 - self.height

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Game Engine ---
class GameEngine:
    def __init__(self, width, height, paddle_sound):
        self.width = width
        self.height = height
        self.player_score = 0
        self.ai_score = 0

        # Ball
        self.ball = Ball(width // 2, height // 2, 10, 10, width, height, paddle_sound)

        # Paddles
        self.player = Paddle(50, height // 2 - 60, 10, 120, 7)
        self.ai = Paddle(width - 60, height // 2 - 60, 10, 120, 5)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed)

    def update(self):
        # Move the ball
        self.ball.move()

        # Check collision with paddles
        self.ball.check_collision([self.player, self.ai])

        # Simple AI for right paddle
        if self.ball.y < self.ai.y:
            self.ai.move(-self.ai.speed)
        elif self.ball.y > self.ai.y + self.ai.height:
            self.ai.move(self.ai.speed)

        # Check if ball goes off the screen (score)
        if self.ball.x < 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.width > self.width:
            self.player_score += 1
            self.ball.reset()

    def render(self, screen):
        # Draw ball
        pygame.draw.rect(screen, (255, 255, 255), self.ball.rect())
        # Draw paddles
        pygame.draw.rect(screen, (255, 255, 255), self.player.rect())
        pygame.draw.rect(screen, (255, 255, 255), self.ai.rect())
        # Draw scores
        font = pygame.font.SysFont(None, 40)
        player_text = font.render(str(self.player_score), True, (255, 255, 255))
        ai_text = font.render(str(self.ai_score), True, (255, 255, 255))
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def reset(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2
