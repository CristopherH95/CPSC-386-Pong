from pygame.sysfont import SysFont
from pygame import mixer


class Board:
    """Generic board class for displaying score type information"""
    def __init__(self, config, screen, text, text_color):
        # display info and config
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.config = config

        # font, text, image settings
        self.text = str(text)
        self.text_color = text_color
        self.font = SysFont(None, 48)
        self.image = None
        self.image_rect = None

    def prep_board(self):
        """Render text as a displayable image"""
        raise NotImplementedError('Objects inheriting from Board must implement a prep_board method')

    def place_board(self):
        """Place the board on the screen"""
        raise NotImplementedError('Objects inheriting from Board must implement a place_board method')

    def show(self):
        """Draw the board to the screen"""
        self.screen.blit(self.image, self.image_rect)


class GoalBoard(Board):
    """Records and displays the required number of points to win a game"""
    def __init__(self, config, screen):
        super().__init__(config, screen, str(config.max_score), (255, 0, 0))

    def prep_board(self):
        """Render text as a displayable image"""
        self.image = self.font.render(self.text, True, self.text_color, self.config.bg_color)
        self.image_rect = self.image.get_rect()
        self.place_board()

    def place_board(self):
        """Place the board on the screen"""
        self.image_rect.x = (self.config.screen_width // 2) - (self.image_rect.width // 2)
        self.image_rect.top = int(self.config.screen_height * 0.15)


class Scoreboard(Board):
    """Records and displays scoring information"""
    def __init__(self, config, screen, player=True):
        super().__init__(config, screen, '0', (255, 255, 255))

        # score sound effect
        self.scoring = mixer.Sound('sounds/pong-score.wav')

        # associated player
        self.player = player
        self.score = 0

        # Initialize
        self.prep_board()

    def reset_score(self):
        """Reset the current score to 0"""
        self.score = 0

    def score_point(self):
        """Add points to the scoreboard"""
        self.score += self.config.score_points
        self.scoring.play()

    def prep_board(self):
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
