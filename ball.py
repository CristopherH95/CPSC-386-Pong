from random import randrange
import pygame
import math


class Ball(pygame.sprite.Sprite):
    """Represents the ball in the pong court, and its related basic physics logic"""
    def __init__(self, config, screen):
        super().__init__()
        # game config info
        self.config = config
        self.screen = screen
        self.game_over = False  # Track game state, as ball behavior changes when a match is over
        # ball dimensions and image
        self.width = config.ball_width
        self.height = config.ball_height
        self.image = pygame.Surface([config.ball_width, config.ball_height])
        self.image.fill(config.ball_color)
        self.rect = self.image.get_rect()
        # ball sounds
        self.paddle_vertical_hit = pygame.mixer.Sound('sounds/pong-paddle-vertical.wav')
        self.paddle_horizontal_hit = pygame.mixer.Sound('sounds/pong-paddle-horizontal.wav')
        # ball 'physics'
        self.speed = 0
        self.speed_increase = 1.1
        self.x = float(0)
        self.y = float(0)
        self.velocity_x = 0
        self.velocity_y = 0
        self.restart_check = None
        self.restart_time = 1000
        self.reset()

    def begin_serve(self):
        """Set restart check to current time measurement to begin waiting for restart"""
        self.restart_check = pygame.time.get_ticks()
        self.x = (self.config.screen_width / 2) - (self.width / 2)
        self.y = self.config.screen_height / 2
        self.rect.x = self.x
        self.rect.y = self.y
        self.velocity_x = 0
        self.velocity_y = 0

    def reset(self):
        """Reset the ball's position and choose a side to 'serve' to"""
        self.x = self.config.screen_width / 2
        self.y = self.config.screen_height / 2
        self.speed = 8.0
        # Choose a side to serve to
        if randrange(2) == 0:
            # random initial velocities
            self.velocity_x = -randrange(self.speed / 2, self.speed)
            self.velocity_y = randrange(-self.speed, self.speed)
        else:
            self.velocity_x = randrange(self.speed / 2, self.speed)
            self.velocity_y = randrange(-self.speed, self.speed)

    def bounce(self, paddle=None):
        """When hitting a surface, calculate the new direction
        and play the paddle hit sound (if not in game over state)"""
        if paddle:
            if paddle.is_horizontal():
                # Calculate new angle from distance from the middle of the paddle on the x-axis
                middle_offset = (self.x + self.width - paddle.rect.x) / (paddle.rect.width + self.width)
                phi = 0.25 * math.pi * (2 * middle_offset - 1)
                self.velocity_x = self.speed * math.sin(phi)
                self.velocity_y = -self.velocity_y
            else:
                # Calculate new angle from distance from the middle of the paddle on the y-axis
                middle_offset = (self.y + self.height - paddle.rect.y) / (paddle.rect.height + self.height)
                phi = 0.25 * math.pi * (2 * middle_offset - 1)
                self.velocity_y = self.speed * math.sin(phi)
                self.velocity_x = -self.velocity_x
        else:
            # If bouncing freely after the game ends, do simple reflect
            if self.rect.y <= 0 or self.rect.y >= self.config.screen_height:
                self.velocity_y = -self.velocity_y
            else:
                self.velocity_x = -self.velocity_x
        self.fix_collisions(paddle)   # prevent ball from getting stuck
        if not self.game_over:  # Disable hit audio when the game is over
            if paddle.is_horizontal():
                self.paddle_horizontal_hit.play()
            else:
                self.paddle_vertical_hit.play()  # play the sound for bouncing off paddle

    def fix_collisions(self, paddle=None):
        """Move the ball to help avoid sprite overlap, or the ball going completely off screen on game over"""
        if paddle:
            if paddle.is_horizontal() and paddle.top:
                self.y += self.height
            elif paddle.is_horizontal():
                self.y -= self.height
            elif self.rect.x < self.config.screen_width / 2:  # Guess which side bounced the ball
                self.x += self.width
            else:
                self.x -= self.width
        else:
            if self.y < 0:
                self.y += self.height
            elif self.y > self.config.screen_height:
                self.y -= self.height
            elif self.x < self.config.screen_width / 2:
                self.x += self.width
            elif self.x > self.config.screen_width / 2:
                self.x -= self.width

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if not self.restart_check:
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.rect.x = self.x
            self.rect.y = self.y
        else:   # If waiting to serve, check that enough time has elapsed
            if abs(self.restart_check - pygame.time.get_ticks()) > self.restart_time:
                self.restart_check = None
                self.reset()
