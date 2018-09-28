import pygame
import sys


def check_events(player_v, player_h1, player_h2):
    """Handles key press events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_v.moving_up = True
            elif event.key == pygame.K_DOWN:
                player_v.moving_down = True
            elif event.key == pygame.K_LEFT:
                player_h1.moving_left = True
                player_h2.moving_left = True
            elif event.key == pygame.K_RIGHT:
                player_h1.moving_right = True
                player_h2.moving_right = True
            elif event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_v.moving_up = False
            elif event.key == pygame.K_DOWN:
                player_v.moving_down = False
            elif event.key == pygame.K_LEFT:
                player_h1.moving_left = False
                player_h2.moving_left = False
            elif event.key == pygame.K_RIGHT:
                player_h1.moving_right = False
                player_h2.moving_right = False


def check_ball_collisions(paddles, ball, config, scoreboard_1, scoreboard_2, game_stats):
    """Check if the ball is colliding with any paddles if the game is still active and bounce.
    If the game is not active, bounce the off the wall instead."""
    if game_stats.game_active:
        paddle_collide = pygame.sprite.spritecollideany(ball, paddles)
        if paddle_collide:
            ball.bounce()
        if ball.rect.x < 0 or (ball.rect.y < 0 and ball.rect.x < (config.screen_width // 2)):
            game_stats.score_for_player()
            scoreboard_2.score_point()
            ball.restart()
        elif ball.rect.x > config.screen_width or \
                (ball.rect.y < 0 and ball.rect.x > (config.screen_width // 2)):
            game_stats.score_for_ai()
            scoreboard_1.score_point()
            ball.restart()
    else:
        if ball.rect.x < 0 or ball.rect.x > config.screen_width:
            ball.bounce()


def check_scores(game_stats):
    """Check the scores to see if anyone has won, if so return True along with the scoreboard
     representing the winner."""
    game_active = True
    winner = None
    if game_stats.player_score > 10 or game_stats.ai_score > 10:
        game_active = False
        winner = 'ply' if game_stats.player_score > 10 else 'ai'
    return game_active, winner


def show_winner(scoreboard):
    """Prepare and blit the winner's scoreboard"""
    scoreboard.prep_winner()
    scoreboard.show_score()


def reset_game(ball, scoreboard_1, scoreboard_2, players, game_stats):
    """Reset the game state so that all scores are 0, paddles are back in default position,
     and the ball is in the default position."""
    ball.restart()
    game_stats.reset_scores()
    scoreboard_1.reset_score()
    scoreboard_2.reset_score()
    for paddle in players.sprites():
        paddle.reset_position()


def update_screen(config, screen, scoreboard_1, scoreboard_2, paddles,
                  ball, ai_player, divider, game_stats, winner=None):
    """Update all graphics, update ball based on collisions."""
    ball.game_over = not game_stats.game_active
    check_ball_collisions(paddles, ball, config, scoreboard_1, scoreboard_2, game_stats)
    screen.fill(config.bg_color)
    divider.draw_divider()
    if game_stats.game_active:
        scoreboard_1.prep_score()
        scoreboard_2.prep_score()
        scoreboard_1.show_score()
        scoreboard_2.show_score()
        for paddle in ai_player.sprites():
            paddle.track_ball(ball)
        paddles.update()
        for paddle in paddles.sprites():
            paddle.blitme()
    else:
        show_winner(scoreboard_1 if winner == 'ai' else scoreboard_2)
    ball.update()
    ball.blitme()
    pygame.display.flip()
