from pygame import mixer


class Config:
    """Stores pygame configurations and settings for various aspects of the game"""
    def __init__(self):
        # display
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # paddles
        self.paddle_speed = 10
        self.paddle_height = 75
        self.paddle_width = 15
        self.paddle_color = (255, 255, 255)
        self.ai_speed = 3

        # ball
        self.ball_height = 10
        self.ball_width = 10
        self.ball_color = (255, 255, 255)
        self.horizontal_bounce_factor = 1.1     # speed increase from horizontal bounce

        # court divider
        self.dash_length = 15
        self.dash_width = 5
        self.line_color = (255, 255, 255)

        # audio
        mixer.init()

        # Scoring
        self.score_points = 1
        self.max_score = 7
