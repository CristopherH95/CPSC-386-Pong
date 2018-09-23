from pygame.sprite import Sprite
from pygame import Surface


class Player(Sprite):
    """Represents a given player's paddle in Pong"""
    def __init__(self, config, screen, player_num=1):
        if not (player_num == 1 or player_num == 2):    # Only 2 players allowed
            raise ValueError("Parameter 'player' can only be 1 or 2")
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.config = config
        self.image = Surface([config.paddle_width, config.paddle_height])
        self.image.fill(config.paddle_color)
        self.rect = self.image.get_rect()
        self.player_num = player_num
        self.reset_position()
        self.moving_up = False
        self.moving_down = False

    def reset_position(self):
        """Reset paddle position based on screen dimensions"""
        if self.player_num == 1:
            self.rect.x = int(self.config.screen_width * 0.1)
        else:
            self.rect.x = int(self.config.screen_width * 0.9)
        self.rect.y = self.config.screen_height // 2

    def update(self):
        """Update paddle's position based on moving state"""
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.config.paddle_speed
        if self.moving_down and self.rect.bottom < self.config.screen_height:
            self.rect.y += self.config.paddle_speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)
