from pygame.sysfont import SysFont
from pygame import Rect


class Button:
    def __init__(self, config, screen, msg):
        self.config = config
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = SysFont(None, 48)
        # Build button rect and center it
        self.rect = Rect(0, 0, self.width, self.height)
        self.rect.centerx = (self.config.screen_width // 2)
        self.rect.centery = int(self.config.screen_height * 0.75)
        # Prep button message only once
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(msg)

    def check_button(self, mouse_x, mouse_y):
        """Check if the given button has been pressed"""
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw button and then draw message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Title:
    """Represents the subtitle text displayed on startup"""
    def __init__(self, bg_color, screen):
        self.bg_color = bg_color
        self.screen = screen
        self.text = 'Pong'
        self.text_color = (255, 255, 255)
        self.font = SysFont(None, 48)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Subtitle:
    """Represents the subtitle text displayed on startup"""
    def __init__(self, bg_color, screen):
        self.bg_color = bg_color
        self.screen = screen
        self.text = 'No Walls'
        self.text_color = (0, 255, 0)
        self.font = SysFont(None, 36)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Intro:
    """Contains information and methods relating to the start menu"""
    def __init__(self, config, game_stats, screen):
        # Config, settings, stats
        self.config = config
        self.game_stats = game_stats
        self.screen = screen

        # text/image information
        self.title = Title(config.bg_color, self.screen)
        self.subtitle = Subtitle(config.bg_color, self.screen)

    def prep_image(self):
        """Render the title as an image"""
        self.title.prep_image()
        self.title.image_rect.centerx = (self.config.screen_width // 2)
        self.title.image_rect.centery = (self.config.screen_height // 2) - self.title.image_rect.height
        self.subtitle.prep_image()
        self.subtitle.image_rect.centerx = (self.config.screen_width // 2)
        self.subtitle.image_rect.centery = (self.config.screen_height // 2) + self.title.image_rect.height

    def show_menu(self):
        """Draw the title to the screen"""
        self.title.blitme()
        self.subtitle.blitme()
