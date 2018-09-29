import pygame
import game_functions as game
from ball import Ball
from court_divider import Divider
from game_stats import GameStats
from paddle import Player, AiPaddleH, AiPaddleV
from scoreboard import Scoreboard
from config import Config


def run_game():
    # initial game setup
    pygame.init()
    config = Config()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (config.screen_width, config.screen_height)
    )
    pygame.display.set_caption('Pong - No Walls')
    # setup players/AI
    ai_player_v = AiPaddleV(config, screen)
    ai_player_h1 = AiPaddleH(config, screen, top=True)
    ai_player_h2 = AiPaddleH(config, screen, top=False)
    player_v = Player(config, screen, vertical=True)
    player_h1 = Player(config, screen, vertical=False, top=True)
    player_h2 = Player(config, screen, vertical=False, top=False)
    paddles = pygame.sprite.Group()
    paddles.add((ai_player_v, ai_player_h1, ai_player_h2,
                 player_v, player_h1, player_h2))
    ai_player = pygame.sprite.Group()
    ai_player.add((ai_player_v, ai_player_h1, ai_player_h2))
    player = pygame.sprite.Group()
    player.add((player_v, player_h1, player_h2))
    # setup scoreboards
    gs = GameStats(config)
    scoreboard_1 = Scoreboard(config, screen, player=False)
    scoreboard_2 = Scoreboard(config, screen, player=True)
    # setup center divider
    divider = Divider(config, screen)
    # setup ball
    ball = Ball(config, screen)
    winner = None

    while True:
        clock.tick(60)  # 60 fps limit
        if not gs.game_active and not winner:
            quit_game = game.startup_screen(config, gs, screen)
            if quit_game:
                pygame.quit()
                break
        gs.game_active, winner = game.check_scores(gs, config)
        if not gs.game_active and winner:   # if game over, display winner for 5 seconds
            game.check_winner_display(gs, ball, scoreboard_1, scoreboard_2, paddles)
        game.check_events(player_v, player_h1, player_h2)
        game.update_screen(config, screen, scoreboard_1, scoreboard_2,
                           paddles, ball, ai_player, divider, gs, winner or None)


if __name__ == '__main__':
    run_game()
