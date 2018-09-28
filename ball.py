import pygame
import math
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
        self.x = float(0)
        self.y = float(0)
        self.direction = 0  # 360 degree direction
        self.restart()

    def restart(self):
        """Reset the ball's position and choose a side to 'serve' to"""
        self.x = self.config.screen_width / 2
        self.y = self.config.screen_height / 2
        self.speed = 8.0
        if randrange(2) == 0:
            self.direction = randrange(-120, -60)
        else:
            self.direction = randrange(60, 120)
        print('random initial direction: ' + str(self.direction))

    def bounce(self):
        """When hitting a vertical surface, calculate the new direction
        and play the paddle hit sound (if not in game over state)"""
        self.direction = (360 - self.direction) % 360
        # self.fix_collisions()
        if not self.game_over:
            self.paddle_hit.play()  # play the sound for bouncing off paddle
        # print('paddle hit direction: ' + str(self.direction))

    def fix_collisions(self):
        """Move the ball on the x-axis to help avoid sprite overlap, or the ball going off screen on game over"""
        if self.rect.x < self.config.screen_width / 2:  # Guess which side bounced the ball
            if not self.game_over:
                self.x = int(self.config.screen_width * 0.1) + self.width
            else:
                self.x += self.width * 2
        else:                                   # Move ball to prevent getting stuck inside paddle
            if not self.game_over:
                self.x = int(self.config.screen_width * 0.9) - self.width
            else:
                self.x -= self.width * 2

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        direction_angle = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_angle)
        self.y -= self.speed * math.cos(direction_angle)
        self.rect.x = self.x
        self.rect.y = self.y
