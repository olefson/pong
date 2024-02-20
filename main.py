import pygame
import math
import pygwidgets
from classes import *
from abc import ABC, abstractmethod
import random

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
ball_started = False

# Text
title = pygwidgets.DisplayText(window, (265, 200), "PONG", fontSize=120, textColor=("white"))

# Buttons
start_button = pygwidgets.TextButton(window, (290, 380), "Start Game", width=200, height=50, fontSize=36)
exit_button = pygwidgets.TextButton(window, (290, 450), "Exit", width=200, height=50, fontSize=36)

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
        global ball_started
        # start moving the ball if the paddle moves
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                ball_started = True

class ComputerPaddle(Paddle):
    def __init__(self, window, x, y, width, height, color):
        super().__init__(window, x, y, width, height, color)
        self.rect = pygame.Rect(x, y, width, height)
        
    def move(self, ball_y): #moves up and down the screen based on ball position
        guessY = ball_y + (-1 if random.random() <= 0.5 else 1) * random.random() * 150
        if self.rect.centery < guessY:
            self.y += 5
        elif self.rect.centery > guessY:
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
        global ball_started
        global P1_score, P2_score #global variables for score
        if self.y <= 0 or self.y >= WINDOW_HEIGHT:
            self.dy *= -1
            return True
        if self.x <= 0 or self.x >= WINDOW_WIDTH:
            self.dx *= -1
            return True
        if player_paddle.rect.collidepoint(self.x, self.y):
            self.dx *= -1  # reverse horizontal direction
            self.x = player_paddle.rect.right + self.radius  # move ball outside the paddle
            return True
        if computer_paddle.rect.collidepoint(self.x, self.y):
            self.dx *= -1
            self.x = computer_paddle.rect.left - self.radius
        if LeftGoal.rect.collidepoint(self.x, self.y):
            P2_score += 1
            P2ScoreDisplay.setValue("Player 2: " + str(P2_score))
            self.x = WINDOW_WIDTH / 2
            self.y = WINDOW_HEIGHT / 2
            ball_started = False
            return False
        if RightGoal.rect.collidepoint(self.x, self.y):
            P1_score += 1
            P1ScoreDisplay.setValue("Player 1: " + str(P1_score))
            self.x = WINDOW_WIDTH / 2
            self.y = WINDOW_HEIGHT / 2
            ball_started = False
            return False
        return False
    
    def handle_event(self, event): #handle collisions
        pass
    


# Game Elements
player_paddle = PlayerPaddle(window, 50, 50, 20, 100, ("white"))
ball = regularBall(window, 400, 300, 10, ("grey"))
ball.dy = 2
ball.dx = -5
computer_paddle = ComputerPaddle(window, 730, 50, 20, 100, ("blue"))
LeftGoal = Goal(window, 0, 0, 50, 600, ("black"))
RightGoal = Goal(window, 750, 0, 50, 600, ("black"))
P1ScoreDisplay = pygwidgets.DisplayText(window, (150, 50), "Player 1: " + str(P1_score), textColor=("white"), fontSize=36)
P2ScoreDisplay = pygwidgets.DisplayText(window, (500, 50), "Player 2: " + str(P2_score), textColor=("white"), fontSize=36)


# Game Loop
run = True

while run:
    window.fill(("black"))
    timer.tick(fps)
    
    # Main Menu
    if menu_state == main_menu:
        title.draw()
        start_button.draw()
        exit_button.draw()
    
        # Main Menu event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if start_button.handleEvent(event):
                menu_state = game
            if exit_button.handleEvent(event):
                run = False
       
    if menu_state == game:
        title = font.render("Game", True, (0, 0, 0))
        window.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 20))
        
        player_paddle.move()
        player_paddle.draw()
        
        computer_paddle.move(ball.y)
        computer_paddle.draw()
        
        LeftGoal.draw()
        RightGoal.draw()
        
        if ball_started:
            ball.move()
        ball.draw()
        
        P1ScoreDisplay.draw()
        P2ScoreDisplay.draw()
        if P1_score >= 5 or P2_score >= 5:
            menu_state = game_over

        # Game event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            ball.handle_event(event)
            player_paddle.handle_event(event)
            
    
    if menu_state == game_over:
        title = font.render("Game Over", True, ("white"))
        window.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 20))
        exit_button.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if exit_button.handleEvent(event):
                run = False
                
            
    pygame.display.update()