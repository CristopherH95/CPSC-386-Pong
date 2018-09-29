from pygame.sysfont import SysFont
from pygame import mixer


class Scoreboard:
    """Records and displays scoring information"""
    def __init__(self, config, screen, player=True):
        # display info and config
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.config = config

        # font, text, image settings
        self.text_color = (255, 255, 255)
        self.font = SysFont(None, 48)
        self.image = None
        self.image_rect = None

        # score sound effect
        self.scoring = mixer.Sound('sounds/pong-score.wav')

        # associated player
        self.player = player
        self.score = 0

        # Initialize
        self.prep_score()

    def reset_score(self):
        """Reset the current score to 0"""
        self.score = 0

    def score_point(self):
        """Add points to the scoreboard"""
        self.score += self.config.score_points
        self.scoring.play()

    def prep_score(self):
        """Render score as a displayable image"""
        score_str = str(self.score)
        self.image = self.font.render(score_str, True, self.text_color, self.config.bg_color)
        self.image_rect = self.image.get_rect()
        self.place_board()

    def place_board(self):
        """Place the scoreboard based on which player the board represents"""
        if self.player:
            self.image_rect.x = int(self.config.screen_width * 0.75)
        else:
            self.image_rect.x = int(self.config.screen_width * 0.25)
        self.image_rect.top = int(self.config.screen_height * 0.05)

    def prep_winner(self):
        """Render a winner announcement instead of a score when a game is over"""
        if self.player:
            message = 'You win!'
        else:
            message = 'Computer wins!'
        self.image = self.font.render(message, True, self.text_color, self.config.bg_color)
        self.image_rect = self.image.get_rect()
        self.place_board()
        self.image_rect.x -= self.image_rect.width // 2

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.image, self.image_rect)
