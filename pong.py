import pygame
import random

pygame.init()
pygame.display.set_caption('Pong')

# Feel free to change width/height
width = 800
height = 500
screen = pygame.display.set_mode((width, height))

background_color = (0, 0, 0)

# Make sure your game operates on same speed, regardless of fps. 
fps = 120
clock = pygame.time.Clock()

font_size = 72
font = pygame.font.Font('font/Pixeltype.ttf', font_size)

def game_loop(score_required_to_win):
    keys = pygame.key.get_pressed()
    game_active = False
    first_time = True

    # Use pygame.K_UP & pygame.K_DOWN for right paddle, and 
    #   pygame.K_w and pygame.K_s for left paddle
    
    # Initialize 2 paddles, and one ball variable 
    dt = clock.tick(fps)/1000
    paddle_1 = Paddle(x=50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_w,
                      down_key=pygame.K_s, color=(255, 100, 100))
    paddle_2 = Paddle(x=width - 50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_UP,
                      down_key=pygame.K_DOWN, color=(100, 255, 100))

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=150, color=(0, 255, 255))
    while True:
        # Exits game if pressed space or tries to quit. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    if not game_active or (not first_time and keys[pygame.K_SPACE]):
                        game_active = True
                        first_time = False
        # Draw background 
        draw_background()
        if game_active:
        # Draw scoreboard 
            draw_scoreboard(score_1=paddle_1.score, score_2=paddle_2.score)
        # Update the two paddles. 
            paddle_1.update(dt)
            paddle_2.update(dt)

        # Update the ball 
            ball.update(dt, paddle_left=paddle_1, paddle_right=paddle_2)

        # Check if a player has won, and if so print which player won, and exit the game (return). 
        #   This should take <10 lines of code (assuming you don't make it more fancy)
            if paddle_1.score == score_required_to_win or paddle_2.score == score_required_to_win:
                game_active = False
        
        # This is neccessary code to see screen updated. 
            pygame.display.update()
        # This is so your game is run at a certain speed. 
        # See: https://www.youtube.com/watch?v=rWtfClpWSb8 for how to achieve true framerate independence. 
        # (Only watch it after you're done with rest of code)
            clock.tick(fps)
        else:
            screen.fill((0, 0, 0))
                            
            font_size = 32
            font1 = pygame.font.Font('font/Pixeltype.ttf', font_size)
            if first_time:
                menutext_surface = font1.render(str("hola amigos, press space to start, esc to quit :< "), True,
                                               (255, 255, 255))
                menutext_rect = menutext_surface.get_rect(center=(width / 2, height / 2))
                screen.blit(menutext_surface, menutext_rect)
            else:
                finalgame_surface = font1.render(str("hola amigos, press space to play again, esc to quit :< "), True,
                                               (255, 255, 255))
                finalgame_rect = finalgame_surface.get_rect(center=(width / 2, height / 2))
                screen.blit(finalgame_surface, finalgame_rect)
                if paddle_1.score == score_required_to_win:
                    winner_surface = font1.render("player 2 won!", True, (255, 255, 255))
                elif paddle_2.score == score_required_to_win:
                    winner_surface = font1.render("player 1 wins!", True, (255, 255, 255))
        
                winner_rect = winner_surface.get_rect(center=(width / 2, height / 2 + 40)) # type: ignore
                screen.blit(winner_surface, winner_rect) # type: ignore

            paddle_1.score = 0
            paddle_2.score = 0

            # Update the display
            pygame.display.update()

def draw_scoreboard(score_1, score_2):
    amount_offset_x = 50
    amount_offset_y = 50
    for (dx, score) in [(-amount_offset_x, score_1), (amount_offset_x, score_2)]:
        text_surface = font.render(str(score), True, "white")
        text_rect = text_surface.get_rect(center=(width // 2 + dx, amount_offset_y))
        screen.blit(text_surface, text_rect)


def draw_background():
    # Fill in the background color, with background_color. 
    #   Do this code first. 
    screen.fill(background_color)
    
    # Draw some gray dotted line in the (vertical) middle
    #   You will want to use a loop for this, and draw lines/rectangles to do so. 
    #   Do this step after getting rest of code done. 
    for x in range(500):
        if x % 20 == 0:
            pygame.draw.line(screen, (255,255,255), (395, x) , (395, x+10), 10)

class Paddle:
    def __init__(self, *, x, y, paddle_width, paddle_height, speed, up_key, down_key, color=(255, 255, 255),
                 border_width=0):
        self.score = 0
        
        #Later on, we will use pygame objects to handle position. 
        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height

        self.speed = abs(speed)

        self.up_key = up_key
        self.down_key = down_key

        self.color = color
        self.border_width = border_width

    def update(self, dt):
        self.move_on_input(dt)
        self.draw()

    def move_on_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            self.y -= self.speed * dt
            if self.y < 0:
                self.y = 0
        elif keys[self.down_key]:
            self.y += self.speed * dt
            if self.y > height - self.height/2:
                self.y = height - self.height/2

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.get_x_low(), self.get_y_low(), self.width, self.height],
                         self.border_width)

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    def get_x_low(self):
        return self.x - self.width / 2

    def get_x_high(self):
        return self.x + self.width / 2

    def get_y_low(self):
        # This is actually the top of the figure (vertically inverted display)
        return self.y - self.height / 2

    def get_y_high(self):
        return self.y + self.height / 2


class Ball:
    def __init__(self, *, x, y, radius, speed_x, color=(255, 255, 255), border_width=0):
        #Later on, we will use pygame objects to handle position (and velocity). 
        self.x = x
        self.y = y

        # This is so that when the paddle gets destroyed, the ball can reset to original pos. 
        self.x_value_to_reset_to = x
        self.y_value_to_reset_to = y

        # Initialize some velocity variables (one for x velocity, one for y)
        #   set the y velocity to be some multiple of the x velocity. 
        #   use sensible naming
        self.vx = speed_x
        self.vy = self.vx * random.uniform(1, 2)

        # Initialize radius, speed_x, color, and border_width class variables. 
        self.radius = radius
        self.color = color
        self.border_width = border_width

    def update(self, dt, *, paddle_left, paddle_right):
        self.move(dt)
        self.account_for_vertical_screen_collision()
        self.account_score_increases(paddle_left, paddle_right)
        # self.does_collide(paddle_right)
        # self.does_collide(paddle_left)
        self.account_for_paddle_collision(paddle_right)
        self.account_for_paddle_collision(paddle_left)
        self.draw()

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.y < self.radius:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y > height - self.radius:
            self.y = height - self.radius
            self.vy = -self.vy
    def draw(self):
        # Draw a pygame circle, with the self.color, self.x, self.y, self.radius, and self.border_width
        #   use the (global) screen variable. 
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)
        
        
    def account_for_paddle_collision(self, paddle: Paddle) -> None:
        """
        Assumes the ball is relatively slow (i.e. won't clip through)
        Also does not use i-frames (i.e. collision could occur multiple times for a collision)
        Simply negates ball
        """

        if not self.does_collide(paddle):
            return 

        # Negates x velocity, if collides with a paddle
        self.vx = -self.vx

    def account_for_vertical_screen_collision(self):
        if self.get_y_low() < 0:
            #We do this, so that it doesn't get potentially stuck out of bounds
            self.set_y_low(0)
            
            #Modify velocity variable. 
            self.vy = -self.vy
        if self.get_y_high() > height:
            # Fill in code. 
            self.set_y_high(0)

            self.vy = -self.vy

    def account_score_increases(self, left_paddle: Paddle, right_paddle: Paddle):
        if self.get_x_low() < 0:
            # Reset ball, increment the right paddle's score. 
            self.reset_ball()
            right_paddle.score += 1
        if self.get_x_high() > width:
            # Fill in code. 
            self.reset_ball()
            left_paddle.score += 1

    def reset_ball(self):
        """
        Flips ball direction, resets position of ball.
        """

        # Flip the x velocity (so the person who scored, has ball sent their way)
        self.vx = -self.vx
        # Set vy to some random multiple of vx.
        self.vy = self.vx * random.uniform(1, 2)

        # This is why we initialized x_value_to_reset_to and y_value_to_reset_to!
        self.x = self.x_value_to_reset_to
        self.y = self.y_value_to_reset_to

    def does_collide(self, paddle):
        # Try and understand what's happening here. 
        #   If you can't, then rewrite separate code which handles collision
        
        # For every point on the ball's bounding square, 
        for point in self.get_points():
            
            # Check if said point is inside the paddle. 
            if paddle.get_x_low() < point[0] < paddle.get_x_high() and paddle.get_y_low() < point[1] < \
                    paddle.get_y_high():
                return True
        return False

    def get_points(self):
        # This does make things scuffed, as circle is essentially treated as a square

        return [(self.get_x_low(), self.get_y_low()),
                (self.get_x_low(), self.get_y_high()),
                (self.get_x_high(), self.get_y_high()),
                (self.get_x_high(), self.get_y_low())]

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    # These will have slightly different implementations than paddle. 

    def get_x_low(self):
        return self.x - self.radius

    def get_x_high(self):
        return self.x + self.radius

    def get_y_low(self):
        return self.y - self.radius

    def get_y_high(self):
        return self.y + self.radius

    def set_x_low(self, num):
        self.x = num + self.radius

    def set_x_high(self, num):
        self.x = num - self.radius

    def set_y_low(self, num):
        self.y = num + self.radius

    def set_y_high(self, num):
        self.y = num - self.radius

# Call the game loop, with some initial amount. 
game_loop(2)
