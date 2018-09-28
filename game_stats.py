

class GameStats:
    """Tracks information about the game state"""
    def __init__(self, config):
        self.config = config
        self.ai_score = 0
        self.player_score = 0
        self.game_active = False

    def reset_scores(self):
        self.ai_score = 0
        self.player_score = 0

    def score_for_player(self):
        self.player_score += 1

    def score_for_ai(self):
        self.ai_score += 1
