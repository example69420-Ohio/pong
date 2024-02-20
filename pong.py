from ast import main
import glob
import math
import pygame
import random
import os

pygame.init()
pygame.display.set_caption('Pong')

# Feel free to change width/height
width = 800
height = 500
screen = pygame.display.set_mode((width, height))

background_color = (0, 0, 0)

bgmusic = pygame.mixer.music.load('audio/Minecraft (mp3cut.net).mp3')
gameovermusic = pygame.mixer.Sound('audio/gameoveraudio.wav')
mainmenumusic = pygame.mixer.Sound('audio/cosmos_adrift.mp3')
# Make sure your game operates on same speed, regardless of fps. 
fps = 60
clock = pygame.time.Clock()

font_size = 72
font = pygame.font.Font('font/Pixeltype.ttf', font_size)
paused = False
pauseserf = pygame.image.load('graphics/pause.png')

def human_game_loop(score_required_to_win):
    global dt
    global width
    global height
    keys = pygame.key.get_pressed()
    game_active = False
    first_time = True
    countdownyes = False
    ballspeed = 150
    # muted = False

    # Use pygame.K_UP & pygame.K_DOWN for right paddle, and 
    #   pygame.K_w and pygame.K_s for left paddle
    
    # Initialize 2 paddles, and one ball variable 
    dt = 1/fps
    paddle_1 = Paddle(x=50, y=height / 2, paddle_width=5, paddle_height=60, speed=300, up_key=pygame.K_w,
                      down_key=pygame.K_s, color=(255, 100, 100))
    paddle_2 = Paddle(x=width - 50, y=height / 2, paddle_width=5, paddle_height=60, speed=300, up_key=pygame.K_UP,
                      down_key=pygame.K_DOWN, color=(100, 255, 100))

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=ballspeed, color=(0, 255, 255))
    pygame.mixer.music.play(loops=-1)
    while True:
        pause()

        if not paused:

            # Exits game if pressed space or tries to quit. 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        # os.system("C:\\Windows\\System32\\shutdown /s /t 100 /c \"why did you leave the game?\"")
                        quit()
                    elif event.key == pygame.K_SPACE:
                        if not game_active or (not first_time and keys[pygame.K_SPACE]):
                            gameovermusic.stop()
                            pygame.mixer.music.play(loops=-1)
                            game_active = True
                            first_time = False
                            countdownyes = False
                    # elif event.key == pygame.K_m:
                    #     if not muted:
                    #         pygame.mixer.music.set_volume(0)
                    #         muted = True
                    #     elif muted:
                    #         pygame.mixer.music.set_volume(100)
                    #         muted = False
                

            # Draw background 
            draw_background()
            if not countdownyes:
                countdown()
                countdownyes = True
            # Draw scoreboard 
            draw_scoreboard(score_1=paddle_1.score, score_2=paddle_2.score)


            # Update the two paddles. 
            paddle_1.update(dt)
            paddle_2.update(dt)

            # Update the ball 
            ball.update(dt, paddle_left=paddle_1, paddle_right=paddle_2)

            # Check if a player has won, and if so print which player won, and exit the game (return). 
            #   This should take <10 lines of code (assuming you don't make it more fancy)
            if paddle_1.score == score_required_to_win:
                gameover(1, score_required_to_win)
            elif paddle_2.score == score_required_to_win:
                gameover(2, score_required_to_win)
            
            # This is neccessary code to see screen updated. 
            pygame.display.update()
            # This is so your game is run at a certain speed. 
            # See: https://www.youtube.com/watch?v=rWtfClpWSb8 for how to achieve true framerate independence. 
            # (Only watch it after you're done with rest of code)
            clock.tick(fps)

def ai_game_loop(score_required_to_win):
    global dt
    global width
    global height
    keys = pygame.key.get_pressed()
    game_active = False
    first_time = True
    countdownyes = False
    # muted = False
    ballspeed = 150

    # Use pygame.K_UP & pygame.K_DOWN for right paddle, and 
    #   pygame.K_w and pygame.K_s for left paddle
    
    # Initialize 2 paddles, and one ball variable 
    dt = 1/fps
    paddle_1 = Paddle(x=50, y=height / 2, paddle_width=5, paddle_height=60, speed=300, up_key=pygame.K_w,
                      down_key=pygame.K_s, color=(255, 100, 100))
    ai_player = AIPlayer(x=width - 50, y=height / 2, paddle_width=5, paddle_height=60, speed=300,
                     up_key=pygame.K_UP, down_key=pygame.K_DOWN, color=(100, 255, 100))

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=ballspeed, color=(0, 255, 255))
    pygame.mixer.music.play(loops=-1)
    while True:
        pause()

        if not paused:
            # Exits game if pressed space or tries to quit. 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        # os.system("C:\\Windows\\System32\\shutdown /s /t 100 /c \"why did you leave the game?\"")
                        quit()
                    elif event.key == pygame.K_SPACE:
                        if not game_active or (not first_time and keys[pygame.K_SPACE]):
                            gameovermusic.stop()
                            pygame.mixer.music.play(loops=-1)
                            game_active = True
                            first_time = False
                            countdownyes = False
                    # elif event.key == pygame.K_m:
                    #     if not muted:
                    #         pygame.mixer.music.set_volume(0)
                    #         muted = True
                    #     elif muted:
                    #         pygame.mixer.music.set_volume(100)
                    #         muted = False

            # Draw background 
            draw_background()
            if not countdownyes:
                countdown()
                countdownyes = True
            # Draw scoreboard 
            draw_scoreboard(score_1=paddle_1.score, score_2=ai_player.paddle.score)


            # Update the two paddles. 
            paddle_1.update(dt)
            ai_player.update(dt, ball)

            # Update the ball 
            ball.update(dt, paddle_left=paddle_1, paddle_right=ai_player.paddle)

            # Check if a player has won, and if so print which player won, and exit the game (return). 
            #   This should take <10 lines of code (assuming you don't make it more fancy)
            if paddle_1.score == score_required_to_win:
                gameover(1, score_required_to_win)
            elif ai_player.paddle.score == score_required_to_win:
                gameover(2, score_required_to_win)
            
            # This is neccessary code to see screen updated. 
            pygame.display.update()
            # This is so your game is run at a certain speed. 
            # See: https://www.youtube.com/watch?v=rWtfClpWSb8 for how to achieve true framerate independence. 
            # (Only watch it after you're done with rest of code)
            clock.tick(fps)

def draw_scoreboard(score_1, score_2):
    amount_offset_x = 50
    amount_offset_y = 50
    for (dx, score) in [(-amount_offset_x, score_1), (amount_offset_x, score_2)]:
        text_surface = font.render(str(score), True, "white")
        text_rect = text_surface.get_rect(center=(width // 2 + dx, amount_offset_y))
        screen.blit(text_surface, text_rect)

def draw_background():
    global width
    # Fill in the background color, with background_color. 
    #   Do this code first. 
    screen.fill(background_color)
    
    # Draw some gray dotted line in the (vertical) middle
    #   You will want to use a loop for this, and draw lines/rectangles to do so. 
    #   Do this step after getting rest of code done. 
    for x in range(500):
        if x % 20 == 0:
            pygame.draw.line(screen, (255,255,255), (width/2, x) , (width/2, x+10), 10)

def countdown():
    global width
    global height
    global dt 
    for countdown in range (3):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 
        screen.fill(background_color)
        countdownserf = font.render(f"{3 - countdown}", True, "white")
        countdownrect = countdownserf.get_rect(center = (width / 2, height / 2))
        screen.blit(countdownserf, countdownrect)
        pygame.display.update()
        pygame.time.wait(1000)
    screen.fill(background_color)
    pygame.display.update()

def pause():
    global paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()  
                else:
                    pygame.mixer.music.unpause()  
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            # elif event.key == pygame.K_m:
            #     if not muted:
            #         pygame.mixer.music.set_volume(0)
            #         muted = True
            #     elif muted:
            #         pygame.mixer.music.set_volume(100)
            #         muted = False

    
    if paused:
        screen.fill((255,255,255))
        pauserec = pauseserf.get_rect(center=(width/2, height/2))
        screen.blit(pauseserf, pauserec)
        pygame.display.update()

def fade_text(text_surface, fade_speed=2):
    # Create a copy of the text surface
    faded_surface = text_surface.copy()
    # Gradually decrease the alpha value of the copied surface
    alpha = 255
    while alpha > 0:
        faded_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(faded_surface, (width/2 - 170 , height/2))
        pygame.display.flip()
        alpha -= fade_speed
        pygame.time.delay(20)

def gameover(whowins, score_to_win):
    pygame.mixer.music.stop()
    screen.fill((0,0,0))
    font_size1 = 32
    font1 = pygame.font.Font('font/Pixeltype.ttf', font_size1)
    font_size2 = 64
    font2 = pygame.font.Font('font/Pixeltype.ttf', font_size2)
    gameovermusic.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cya = font2.render("SEE YOU NEXT TIME", False, (255, 255, 255))
                    fade_text(cya)
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if replay.is_over(pos):
                    gameovermusic.stop()
                    defaultmain(score_to_win)
                    
        replay = Button(350, height/2, 100, 40, 10, (255, 255, 255), 'replay', font1, (0,0,0))

        if whowins == 1:
            winner = font1.render("Player 1 wins!", False, (255, 255, 255))
        elif whowins == 2:
            winner = font1.render("Player 2 won!", False, (255,255,255))
        
        winnerrect = winner.get_rect(center = (width/2, height/2 - 100))
        replay.draw(screen)
        screen.blit(winner, winnerrect)
        pygame.display.update()

def defaultmain(score_to_win):
    # muted = False
    n = 1
    font_size1 = 32
    font1 = pygame.font.Font('font/Pixeltype.ttf', font_size1)
    font_size2 = 64
    font2 = pygame.font.Font('font/Pixeltype.ttf', font_size2)
    while True:
        screen.fill((0, 0, 0))
        pongserf = font2.render("PONG", False, (255, 255, 255))
        rotated_pongserf = pygame.transform.rotate(pongserf, math.sin(n)) 
        screen.blit(rotated_pongserf, (350, 100))

        player1 = Button(150, height/2, 100, 40, 10, (255, 255, 255), '1 Player', font1, (0,0,0))
        player2 = Button(550, height/2, 100, 40, 10, (255, 255, 255), '2 Player', font1, (0,0,0))
        # mute = Button(700, 450, 100, 50, 10, (255, 255, 255), 'Mute', font1, (0,0,0))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if player2.is_over(pos):
                        mainmenumusic.stop()
                        human_game_loop(score_to_win)
                    if player1.is_over(pos):
                        mainmenumusic.stop()
                        ai_game_loop(score_to_win)
                    # if mute.is_over(pos):
                    #     if not muted: 
                    #         mainmenumusic.set_volume(0)
                    #         muted = True
                    #     elif muted:
                    #         mainmenumusic.set_volume(100)
                    #         muted = False

                        
        n+=10
        player1.draw(screen)
        player2.draw(screen)
        # mute.draw(screen)
        pygame.display.update()

def mainmenu(score_to_win):
    # muted = False
    n = 1
    mainmenumusic.play(loops=-1)
    font_size1 = 32
    font1 = pygame.font.Font('font/Pixeltype.ttf', font_size1)
    font_size2 = 64
    font2 = pygame.font.Font('font/Pixeltype.ttf', font_size2)
    while True:
        screen.fill((0, 0, 0))
        pongserf = font2.render("PONG", False, (255, 255, 255))
        rotated_pongserf = pygame.transform.rotate(pongserf, math.sin(n)) 
        screen.blit(rotated_pongserf, (350, 100))

        start = Button(350, height/2, 100, 40, 10, (255, 255, 255), 'start', font1, (0,0,0))
        # mute = Button(700, 450, 100, 50, 10, (255, 255, 255), 'Mute', font1, (0,0,0))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if start.is_over(pos):
                        defaultmain(score_to_win)
                    # if mute.is_over(pos):
                    #     if not muted: 
                    #         mainmenumusic.set_volume(0)
                    #         muted = True
                    #     elif muted:
                    #         mainmenumusic.set_volume(100)
                    #         muted = False
        n+=10
        start.draw(screen)
        # mute.draw(screen)
        pygame.display.update()

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
        self.vy = 0
        self.max_acceleration = 300

    def update(self, dt):
        self.move_on_input(dt)
        self.draw()

    # def move_on_input(self, dt):
    #     keys = pygame.key.get_pressed()
    #     if keys[self.up_key]:
    #         self.vy -= self.speed*dt      
    #     elif keys[self.down_key]:
    #         self.vy += self.speed * dt

    #     self.vy = max(-self.max_acceleration, min(self.max_acceleration, self.vy))
    #     self.vy *= 0.8 
    #     self.y += self.vy 
        
        
    #     if self.y < self.height / 2:
    #         self.y = self.height / 2
    #         self.vy = 0
    #     elif self.y > height - self.height/2:
    #         self.y = height - self.height/2
    #         self.vy = 0
    def move_on_input(self, dt):
        keys = pygame.key.get_pressed()
    
        acceleration = self.speed + 800
        deceleration = 800 

        if keys[self.up_key]:
            self.vy -= acceleration * dt
        elif keys[self.down_key]:
            self.vy += acceleration * dt
        else:
            if self.vy > 0:
                self.vy -= deceleration * dt
            elif self.vy < 0:
                self.vy += deceleration * dt

        self.vy *= 0.5**dt 

        self.y += self.vy * dt

        if self.y < self.height / 2:
            self.y = self.height / 2
            self.vy = 0
        elif self.y > height - self.height / 2:
            self.y = height - self.height / 2
            self.vy = 0

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
        self.initialx =speed_x
        self.vx = speed_x 
        self.vy = self.vx * random.uniform(1, 2)
        self.initial_vy_ratio = random.uniform(1, 2)
        self.speed_increase_rate = 0.1

        # Initialize radius, speed_x, color, and border_width class variables. 
        self.radius = radius
        self.color = color
        self.border_width = border_width
        self.trail_particle_systems = []


    def update(self, dt, *, paddle_left, paddle_right):
        self.move(dt)
        self.account_for_vertical_screen_collision()
        self.account_score_increases(paddle_left, paddle_right)
        self.vx += self.speed_increase_rate * dt
        self.account_for_paddle_collision(paddle_right)
        self.account_for_paddle_collision(paddle_left)
        self.trail_particle_systems.append(ParticleSystem((self.x, self.y), 1, (255, 255, 255)))

        # Update existing particle systems in the trail
        for particle_system in self.trail_particle_systems:
            particle_system.update()

        # Keep only the last 100 particle systems in the trail to avoid memory overflow
        self.trail_particle_systems = self.trail_particle_systems[-100:]
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

    def speedreset(self):
        self.vx = self.initialx
        self.vy = self.vx * random.uniform(1, 2)


    def draw(self):
        # Draw a pygame circle, with the self.color, self.x, self.y, self.radius, and self.border_width
        #   use the (global) screen variable. 
        for particle_system in self.trail_particle_systems:
            particle_system.draw(screen)
        
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)

        
        
    def account_for_paddle_collision(self, paddle: Paddle) -> None:
        if not self.does_collide(paddle):
            return

        # Modify x velocity based on which paddle the ball collides with
        if paddle.get_x_low() < self.x < paddle.x:
            self.vx = abs(self.vx)  # Collided with the left paddle, set x velocity to its absolute value
        elif paddle.x < self.x < paddle.get_x_high():
            self.vx = -abs(self.vx)  # Collided with the right paddle, set x velocity to its negated absolute value

        # Calculate the distance from the paddle's center to the ball's center
        distance_from_center = self.y - paddle.y
        bounce_factor = 0.2  # Adjust this factor to control the influence of distance_from_center  

        # Normalize the distance to a value between -1 and 1
        normalized_distance = distance_from_center / (paddle.height * bounce_factor)

        # Adjust the angle of reflection based on the normalized distance
        angle = normalized_distance * (math.pi / 4)  # Adjust the coefficient to change the bounce angle

        # Calculate the new velocity components based on the angle
        new_vx = self.vx * math.cos(angle) - self.vy * math.sin(angle)
        new_vy = self.vx * math.sin(angle) + self.vy * math.cos(angle)

        # Update the velocity components
        self.vx = new_vx
        self.vy = new_vy

        # Ensure the ball's position stays within the screen boundaries
        if self.y < self.radius:
            self.y = self.radius
        elif self.y > height - self.radius:
            self.y = height - self.radius


        

    def reset_speed_and_angle(self):
        # Reset speed and angle to their initial values
        self.vx = self.initialx
        self.vy = self.initialx * self.initial_vy_ratio

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
        self.reset_speed_and_angle()


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

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, radius, color, text, font, text_color):
        super().__init__()  # Call superclass constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color

    def draw_rounded_rect(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect, border_radius=self.radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw(self, screen):
        self.draw_rounded_rect(screen)

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class AIPlayer:
    def __init__(self, x, y, paddle_width, paddle_height, speed, up_key, down_key, color=(255, 255, 255),
                 border_width=0):
        self.paddle = Paddle(x=x, y=y, paddle_width=paddle_width, paddle_height=paddle_height, speed=speed,
                            up_key=up_key, down_key=down_key, color=color,
                             border_width=border_width)

    def update(self, dt, ball):
        predicted_ball_y = ball.y + (ball.y - self.paddle.y) * (self.paddle.x - ball.x) / ball.vx

        predicted_ball_y += random.uniform(-75, 75)

        # Move the AI paddle towards the predicted position
        acceleration = self.paddle.speed + 800
        deceleration = 800 

        if predicted_ball_y < self.paddle.y:
            self.paddle.vy -= acceleration * dt
        elif predicted_ball_y > self.paddle.y:
            self.paddle.vy += acceleration * dt
        else:
            if self.paddle.vy > 0:
                self.paddle.vy -= deceleration * dt
            elif self.paddle.vy < 0:
                self.paddle.vy += deceleration * dt

        self.paddle.vy *= 0.5**dt 

        self.paddle.y += self.paddle.vy * dt

        # Ensure the AI paddle stays within the screen boundaries
        if self.paddle.y < self.paddle.height / 2:
            self.paddle.y = self.paddle.height / 2
            self.paddle.vy = 0
        elif self.paddle.y > height - self.paddle.height / 2:
            self.paddle.y = height - self.paddle.height / 2
            self.paddle.vy = 0

        self.paddle.draw()
    def draw(self):
        self.paddle.draw()

class Particle:
    def __init__(self, position, color, lifespan, fade_rate):
        self.x, self.y = position
        # Validate the color argument
        if isinstance(color, tuple) and len(color) == 3:
            # Ensure each component is within the valid range of 0 to 255
            self.color = tuple(max(0, min(255, c)) for c in color)
        else:
            # Default to white if color argument is invalid
            self.color = (255, 255, 255)
        self.radius = 2
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.gravity = 0.1
        self.lifespan = lifespan  # Decrease lifespan to make particles disappear faster
        self.fade_rate = fade_rate  # Increase fade rate to make particles fade faster

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1

    def draw(self, screen):
        alpha = max(0, min(255, int(self.lifespan * self.fade_rate)))  # Ensure alpha is 0-255
        color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(screen, color_with_alpha, (int(self.x), int(self.y)), self.radius)

class ParticleSystem:
    def __init__(self, position, num_particles, color):
        self.position = position
        self.num_particles = num_particles
        self.color = color
        self.particles = [Particle(position, color, 25, 200) for _ in range(num_particles)]

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
            
#  Call the game loop, with some initial amount. 
mainmenu(2)
