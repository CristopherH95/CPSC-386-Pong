from pygame import draw


class Divider:
    """Represents the dashed line dividing the middle of the pong court"""
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.x = config.screen_width // 2
        self.dash = config.dash_length
        self.width = config.dash_width

    def draw_divider(self):
        """Draw a series of line segments to create a dashed line divider"""
        for i in range(0, self.config.screen_height, int(self.dash * 2)):
            draw.line(self.screen, self.config.line_color, (self.x, i), (self.x, i + self.dash), self.width)
