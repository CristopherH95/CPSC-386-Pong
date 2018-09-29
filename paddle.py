from pygame.sprite import Sprite
from pygame import Surface


class Paddle(Sprite):
    """Base class for paddles in the game"""
    def __init__(self, config, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.config = config
        self.image = Surface([config.paddle_width, config.paddle_height])
        self.image.fill(config.paddle_color)
        self.rect = self.image.get_rect()

    def get_middle(self):
        if self.is_horizontal():
            return self.rect.width / 2
        else:
            return self.rect.height / 2

    def is_horizontal(self):
        return self.rect.width > self.rect.height

    def reset_position(self):
        raise NotImplemented('Paddle subclasses must implement reset_position method')

    def blitme(self):
        """Blit the paddle to the screen"""
        self.screen.blit(self.image, self.rect)


class AiPaddleH(Paddle):
    """Represents a horizontal AI Paddle"""
    def __init__(self, config, screen, top=True):
        super().__init__(config, screen)
        self.image = Surface([config.paddle_height, config.paddle_width])
        self.image.fill(config.paddle_color)
        self.rect = self.image.get_rect()
        self.speed = config.ai_speed
        self.top = top
        self.reset_position()

    def reset_position(self):
        self.rect.x = (self.config.screen_width // 2) // 2
        if self.top:
            self.rect.y = int(self.config.screen_height * 0.005)
        else:
            self.rect.y = int(self.config.screen_height * 0.975)

    def track_ball(self, ball):
        if self.rect.x > ball.rect.x and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.rect.x < ball.rect.x and \
                self.rect.right < (self.config.screen_width // 2):
            self.rect.x += self.speed


class AiPaddleV(Paddle):
    """Represents a vertical AI Paddle"""
    def __init__(self, config, screen):
        super().__init__(config, screen)
        self.speed = config.ai_speed
        self.reset_position()

    def reset_position(self):
        self.rect.x = int(self.config.screen_width * 0.005)
        self.rect.y = self.config.screen_height // 2

    def track_ball(self, ball):
        if self.rect.centery > ball.rect.y and self.rect.top > 0:
            self.rect.centery -= self.speed
        if self.rect.centery < ball.rect.y and self.rect.bottom < self.config.screen_height:
            self.rect.centery += self.speed


class Player(Paddle):
    """Represents a player's paddle in the game"""
    def __init__(self, config, screen, vertical=True, top=True):
        super().__init__(config, screen)
        self.vertical = vertical
        if not self.vertical:
            self.image = Surface([config.paddle_height, config.paddle_width])
            self.image.fill(config.paddle_color)
            self.rect = self.image.get_rect()
        self.top = top
        self.reset_position()
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def reset_position(self):
        """Reset paddle position based on screen dimensions"""
        if self.vertical:
            self.rect.x = int(self.config.screen_width * 0.975)
            self.rect.y = self.config.screen_height // 2
        else:
            self.rect.x = int(self.config.screen_width * 0.75)
            if self.top:
                self.rect.y = int(self.config.screen_height * 0.005)
            else:
                self.rect.y = int(self.config.screen_height * 0.975)

    def update(self):
        """Update paddle's position based on moving state"""
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.config.paddle_speed
        if self.moving_down and self.rect.bottom < self.config.screen_height:
            self.rect.y += self.config.paddle_speed
        if self.moving_left and self.rect.left > (self.config.screen_width // 2):
            self.rect.x -= self.config.paddle_speed
        if self.moving_right and self.rect.right < self.config.screen_width:
            self.rect.x += self.config.paddle_speed
