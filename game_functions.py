import pygame
import sys


def check_events(player1, player2):
    """Handles key press events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2.moving_up = True
            elif event.key == pygame.K_w:
                player1.moving_up = True
            elif event.key == pygame.K_DOWN:
                player2.moving_down = True
            elif event.key == pygame.K_s:
                player1.moving_down = True
            elif event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2.moving_up = False
            elif event.key == pygame.K_w:
                player1.moving_up = False
            elif event.key == pygame.K_DOWN:
                player2.moving_down = False
            elif event.key == pygame.K_s:
                player1.moving_down = False


def check_ball_collisions(screen, players, ball, config, scoreboard_1, scoreboard_2, game_over):
    """Check if the ball is colliding with any paddles if the game is still active and bounce.
    If the game is not active, bounce the off the wall instead."""
    if not game_over:
        paddle_collide = pygame.sprite.spritecollideany(ball, players)
        if paddle_collide:
            ball.bounce()
        if ball.rect.x < 0:
            scoreboard_2.score_point()
            ball.restart()
        elif ball.rect.x > config.screen_width:
            scoreboard_1.score_point()
            ball.restart()
    else:
        if ball.rect.x < 0 or ball.rect.x > config.screen_width:
            ball.bounce()


def check_scores(scoreboard_1, scoreboard_2):
    """Check the scores to see if anyone has won, if so return True along with the scoreboard
     representing the winner."""
    game_over = False
    winner = None
    if scoreboard_1.score > 10 or scoreboard_2.score > 10:
        game_over = True
        winner = scoreboard_1 if scoreboard_1.score > 10 else scoreboard_2
    return game_over, winner


def show_winner(scoreboard):
    """Prepare and blit the winner's scoreboard"""
    scoreboard.prep_winner()
    scoreboard.show_score()


def reset_game(ball, scoreboard_1, scoreboard_2, players):
    """Reset the game state so that all scores are 0, paddles are back in default position,
     and the ball is in the default position."""
    ball.restart()
    scoreboard_1.reset_score()
    scoreboard_2.reset_score()
    for paddle in players.sprites():
        paddle.reset_position()


def update_screen(config, screen, scoreboard_1, scoreboard_2, players, ball, divider, game_over, winner=None):
    """Update all graphics, update ball based on collisions."""
    ball.game_over = game_over
    check_ball_collisions(screen, players, ball, config, scoreboard_1, scoreboard_2, game_over)
    screen.fill(config.bg_color)
    divider.draw_divider()
    if not game_over:
        scoreboard_1.prep_score()
        scoreboard_2.prep_score()
        scoreboard_1.show_score()
        scoreboard_2.show_score()
        players.update()
        for paddle in players.sprites():
            paddle.blitme()
    else:
        show_winner(winner)
    ball.update()
    ball.blitme()
    pygame.display.flip()
