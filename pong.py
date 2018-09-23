import pygame
import game_functions as game
from ball import Ball
from court_divider import Divider
from player import Player
from scoreboard import Scoreboard
from config import Config


def run_game():
    pygame.init()
    config = Config()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (config.screen_width, config.screen_height)
    )
    pygame.display.set_caption('Pong')
    # setup players
    player1 = Player(config, screen, player_num=1)
    player2 = Player(config, screen, player_num=2)
    players = pygame.sprite.Group()
    players.add((player1, player2))
    # setup scoreboards
    scoreboard_1 = Scoreboard(config, screen, player1)
    scoreboard_2 = Scoreboard(config, screen, player2)
    # setup center divider
    divider = Divider(config, screen)
    # setup ball
    ball = Ball(config, screen)
    game_over = False
    winner_time = None

    while True:
        clock.tick(60)  # 60 fps limit
        game_over, winner = game.check_scores(scoreboard_1, scoreboard_2)
        if game_over:   # if game over, display winner for 5 seconds
            if winner_time is None:
                winner_time = pygame.time.get_ticks()
            if abs(winner_time - pygame.time.get_ticks()) > 5000:
                game_over, winner_time = False, None
                game.reset_game(ball, scoreboard_1, scoreboard_2, players)
        game.check_events(player1, player2)
        game.update_screen(config, screen, scoreboard_1, scoreboard_2,
                           players, ball, divider, game_over, winner or None)


if __name__ == '__main__':
    run_game()
