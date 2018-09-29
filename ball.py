import pygame
from random import randrange


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
        self.paddle_hit = pygame.mixer.Sound('sounds/pong-paddle.wav')
        self.border_hit = pygame.mixer.Sound('sounds/pong-border.wav')
        # ball 'physics'
        self.speed = 0
        self.speed_increase = 1.1
        self.x = float(0)
        self.y = float(0)
        self.velocity_x = 0
        self.velocity_y = 0
        self.restart()

    def restart(self):
        """Reset the ball's position and choose a side to 'serve' to"""
        self.x = self.config.screen_width / 2
        self.y = self.config.screen_height / 2
        self.speed = 8.0
        if randrange(2) == 0:
            self.velocity_x = -self.speed
            self.velocity_y = randrange(-self.speed, self.speed)
        else:
            self.velocity_x = self.speed
            self.velocity_y = randrange(-self.speed, self.speed)

    def bounce(self, paddle=None):
        """When hitting a surface, calculate the new direction
        and play the paddle hit sound (if not in game over state)"""
        if paddle:
            if paddle.is_horizontal():
                self.velocity_y = -self.velocity_y
            else:
                self.velocity_x = -self.velocity_x
        else:
            if self.rect.y <= 0 or self.rect.y >= self.config.screen_height:
                self.velocity_y = -self.velocity_y
            else:
                self.velocity_x = -self.velocity_x
        self.fix_collisions(paddle)
        if not self.game_over:
            self.paddle_hit.play()  # play the sound for bouncing off paddle

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
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.x = self.x
        self.rect.y = self.y
