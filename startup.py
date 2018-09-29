from pygame.sysfont import SysFont


class Startup:
    """Contains information and methods relating to the start menu"""
    def __init__(self, config, game_stats, screen):
        # Config, settings, stats
        self.config = config
        self.game_stats = game_stats
        self.screen = screen

        # text/image information
        self.title = 'Pong'
        self.text_color = (255, 255, 255)
        self.font = SysFont(None, 48)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the title as an image"""
        self.image = self.font.render(self.title, True, self.text_color, self.config.bg_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = self.config.screen_width // 2
        self.image_rect.y = self.config.screen_height // 2

    def show_menu(self):
        """Draw the title to the screen"""
        self.screen.blit(self.image, self.image_rect)
