Pong -- No Walls in Pygame
written by Cristopher Hernandez

First to score 7 points is the winner. The player controls horizontal paddles with left and right arrow keys.
The vertical paddle is controlled with the up and down arrow keys. The AI opponent will track the ball to attempt
to beat the player. The Red number in the middle of the screen represents the score needed to win the game.

Note: The ball's angle depends on where on the paddle the ball collides. Hitting the ball at the extreme ends
      of the paddle increases the angle (and potentially also the speed). Hitting the ball towards the middle
      causes the ball to be reflected in more of a straight line.


To run the game: execute pong.py (e.g. run 'python pong.py' on the command line)

Player controls:

'Up' --> Move vertical paddle up
'Down' --> Move vertical paddle down
'Left' --> Move horizontal paddles left
'Right' --> Move horizontal paddles right
