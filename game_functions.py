from paddle import Player, AiPaddleH, AiPaddleV
from intro import Button, Intro
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


def setup_players(config, screen):
    """Return a dictionary containing all relevant objects for the AI player and human player"""
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
    return {
        'ai_player_v': ai_player_v,
        'ai_player_h1': ai_player_h1,
        'ai_player_h2': ai_player_h2,
        'player_v': player_v,
        'player_h1': player_h1,
        'player_h2': player_h2,
        'paddles': paddles,
        'ai_player': ai_player,
        'player': player
    }


def check_ball_collisions(paddles, ball, config, scoreboard_1, scoreboard_2, game_stats):
    """Check if the ball is colliding with any paddles if the game is still active and bounce.
    If the game is not active, bounce the off the wall instead."""
    if game_stats.game_active:
        paddle_collide = pygame.sprite.spritecollideany(ball, paddles)
        if paddle_collide:
            ball.bounce(paddle_collide)
        if ball.rect.x < 0 or \
                ((ball.rect.y < 0 or ball.rect.y > config.screen_height)
                 and ball.rect.x < (config.screen_width // 2)):
            game_stats.score_for_player()
            scoreboard_2.score_point()
            scoreboard_2.prep_score()
            ball.begin_serve()
        elif ball.rect.x > config.screen_width or \
                ((ball.rect.y < 0 or ball.rect.y > config.screen_height)
                 and ball.rect.x > (config.screen_width // 2)):
            game_stats.score_for_ai()
            scoreboard_1.score_point()
            scoreboard_1.prep_score()
            ball.begin_serve()
    else:
        if (ball.rect.x < 0 or ball.rect.x > config.screen_width) or \
                (ball.rect.y < 0 or ball.rect.y > config.screen_height):
            ball.bounce()


def check_scores(game_stats, config):
    """Check the scores to see if anyone has won, if so return True along with the scoreboard
     representing the winner."""
    game_active = True
    winner = None
    if game_stats.player_score >= config.max_score or game_stats.ai_score >= config.max_score:
        game_active = False
        winner = 'ply' if game_stats.player_score >= config.max_score else 'ai'
    return game_active, winner


def check_winner_display(game_stats, ball, scoreboard_1, scoreboard_2, paddles):
    """Check the amount of time the winner has been displayed, reset if longer than 5 seconds, return True if reset"""
    done = False
    if game_stats.winner_time is None:
        game_stats.winner_time = pygame.time.get_ticks()
    if abs(game_stats.winner_time - pygame.time.get_ticks()) > 6000:  # winner should be displayed for 6 seconds
        done = True
        game_stats.winner_time = None
        reset_game(ball, scoreboard_1, scoreboard_2, paddles, game_stats)
    return done


def show_winner(scoreboard):
    """Prepare and blit the winner's scoreboard"""
    scoreboard.prep_winner()
    scoreboard.show_score()


def reset_game(ball, scoreboard_1, scoreboard_2, players, game_stats):
    """Reset the game state so that all scores are 0, paddles are back in default position,
     and the ball is in the default position."""
    ball.reset()
    game_stats.reset_scores()
    scoreboard_1.reset_score()
    scoreboard_2.reset_score()
    scoreboard_1.prep_score()
    scoreboard_2.prep_score()
    for paddle in players.sprites():
        paddle.reset_position()


def startup_screen(config, game_stats, screen):
    """Display an introductory startup screen for the game"""
    title_screen = Intro(config, game_stats, screen)
    title_screen.prep_image()
    button = Button(config, screen, 'Play')
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                game_stats.game_active = button.check_button(click_x, click_y)
                intro = not game_stats.game_active
        screen.fill(config.bg_color)
        title_screen.show_menu()
        button.draw_button()
        pygame.display.flip()

    return False


def update_screen(config, screen, scoreboard_1, scoreboard_2, paddles,
                  ball, ai_player, divider, game_stats, winner=None):
    """Update all graphics, update ball based on collisions."""
    ball.game_over = not game_stats.game_active
    check_ball_collisions(paddles, ball, config, scoreboard_1, scoreboard_2, game_stats)
    screen.fill(config.bg_color)
    divider.draw_divider()
    if game_stats.game_active:
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
