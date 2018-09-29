import pygame
import game_functions as game
from ball import Ball
from court_divider import Divider
from game_stats import GameStats
from scoreboard import Scoreboard, GoalBoard
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
    player_data = game.setup_players(config, screen)
    # setup scoreboards
    gs = GameStats(config)
    scoreboard_1 = Scoreboard(config, screen, player=False)
    scoreboard_2 = Scoreboard(config, screen, player=True)
    goal_board = GoalBoard(config, screen)
    goal_board.prep_board()
    # setup center divider
    divider = Divider(config, screen)
    # setup ball
    ball = Ball(config, screen)
    winner = None

    while True:
        clock.tick(60)  # 60 fps limit
        if not gs.game_active and not winner:
            quit_game = not game.startup_screen(config, gs, screen)
            if quit_game:
                pygame.quit()
                break
        gs.game_active, winner = game.check_scores(gs, config)
        if not gs.game_active and winner:   # if game over, display winner for 5 seconds
            if game.check_winner_display(gs, ball, scoreboard_1, scoreboard_2, player_data['paddles']):
                winner = None
                continue
        game.check_events(player_data['player_v'], player_data['player_h1'], player_data['player_h2'])
        game.update_screen(config, screen, scoreboard_1, scoreboard_2,
                           player_data['paddles'], ball, player_data['ai_player'], divider, gs, goal_board,
                           winner or None)


if __name__ == '__main__':
    run_game()
