import pygame
import math
import pygwidgets
from classes import *
from abc import ABC, abstractmethod

# Create Display Window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
timer = pygame.time.Clock() #load the clock
fps = 60
font = pygame.font.Font(None, 36)

# Game States
main_menu = "main"
game = "game"
game_over = "game_over"
menu_state = main_menu

# Trackers
P1_score = 0
P2_score = 0


# Buttons
start_button = pygwidgets.TextButton(window, (WINDOW_WIDTH / 2 - 100, 100), "Start Game")
exit_button = pygwidgets.TextButton(window, (WINDOW_WIDTH / 2 - 100, 200), "Exit Game")

# Game classes
class PlayerPaddle(Paddle):
    def __init__(self, window, x, y, width, height, color):
        super().__init__(window, x, y, width, height, color)
        self.rect = pygame.Rect(x, y, width, height)
        
    def move(self): #moves up and down the screen based on arrow key input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5
        # update rect
        self.rect.y = self.y
        
    
    def handle_event(self, event):
        pass

class ComputerPaddle(Paddle):
    def __init__(self, window, x, y, width, height, color):
        super().__init__(window, x, y, width, height, color)
        self.rect = pygame.Rect(x, y, width, height)
        
    def move(self, ball_y): #moves up and down the screen based on ball position
        if self.rect.centery < ball_y:
            self.y += 5
        elif self.rect.centery > ball_y:
            self.y -= 5
        
        # add boundry checking
        if self.y < 0:
            self.y = 0
        elif self.y > WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height
            
        # update rect
        self.rect.y = self.y
    
    def handle_event(self, event):
        pass

class regularBall(Ball):
    def __init__(self, window, x, y, radius, color):
        super().__init__(window, x, y, radius, color)
        self.rect = pygame.Rect(x, y, radius, radius)
        
    def move(self): #moves the ball
        steps = 10
        step_dx = self.dx / steps
        step_dy = self.dy / steps
        
        for i in range(steps):
            # move ball one step forward
            self.x += step_dx
            self.y += step_dy
            
            # check for collision with walls
            if self.check_collision():
                break
            
    def check_collision(self): #checks for collision with walls
        global P1_score, P2_score #global variables for score
        if self.y <= 0 or self.y >= WINDOW_HEIGHT:
            self.dy *= -1
            return True
        if self.x <= 0 or self.x >= WINDOW_WIDTH:
            self.dx *= -1
            return True
        if player_paddle.rect.collidepoint(self.x, self.y):
            self.dx *= -1  # Reverse horizontal direction
            self.x = player_paddle.rect.right + self.radius  # Move the ball outside the paddle
            return True
        if computer_paddle.rect.collidepoint(self.x, self.y):
            self.dx *= -1
            self.x = computer_paddle.rect.left - self.radius
        if LeftGoal.rect.collidepoint(self.x, self.y):
            P2_score += 1
            P2ScoreDisplay.setValue("Player 2: " + str(P2_score))
            self.x = WINDOW_WIDTH / 2
            self.y = WINDOW_HEIGHT / 2
            return False
        if RightGoal.rect.collidepoint(self.x, self.y):
            P1_score += 1
            P1ScoreDisplay.setValue("Player 1: " + str(P1_score))
            self.x = WINDOW_WIDTH / 2
            self.y = WINDOW_HEIGHT / 2
            return False
        return False
    
    def handle_event(self, event): #handle collisions
        pass
    


# Game Elements
player_paddle = PlayerPaddle(window, 50, 50, 20, 100, (0, 0, 0))
ball = regularBall(window, 400, 300, 10, (0, 0, 0))
computer_paddle = ComputerPaddle(window, 730, 50, 20, 100, ("blue"))
# RightWall = GiantRightWall(window, 700, 0, 50, 600, (0, 0, 0))
LeftGoal = Goal(window, 0, 0, 50, 600, ("red"))
RightGoal = Goal(window, 750, 0, 50, 600, ("red"))
P1ScoreDisplay = pygwidgets.DisplayText(window, (WINDOW_WIDTH / 2 - 100, 50), "Player 1: " + str(P1_score))
P2ScoreDisplay = pygwidgets.DisplayText(window, (WINDOW_WIDTH / 2 + 100, 50), "Player 2: " + str(P2_score))



# Game Loop
run = True

while run:
    window.fill((255, 255, 255))
    timer.tick(fps)
    
    # Main Menu
    if menu_state == main_menu:
        title = font.render("Main Menu", True, (0, 0, 0))
        window.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 20))
        start_button.draw()
    
        # Main Menu event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if start_button.handleEvent(event):
                menu_state = game
       
    if menu_state == game:
        title = font.render("Game", True, (0, 0, 0))
        window.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 20))
        exit_button.draw()
        
        player_paddle.move()
        player_paddle.draw()
        
        computer_paddle.move(ball.y)
        computer_paddle.draw()
        
        LeftGoal.draw()
        RightGoal.draw()
        
        ball.move()
        ball.draw()
        P1ScoreDisplay.draw()
        P2ScoreDisplay.draw()
        # Game event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if exit_button.handleEvent(event):
                run = False
            ball.handle_event(event)
                
            
    pygame.display.update()