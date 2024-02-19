import pygame
import math
import pygwidgets
from classes import Paddle, Ball
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

# Abstract Classes
class Ball(ABC): #abstract class for the ball types
    def __init__(self, window, x, y, radius, color):
        self.window = window
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.dx = 5
        self.dy = 5
        
    @abstractmethod
    def move(self): #moves the ball
        pass
    
    @abstractmethod
    def handle_event(self, event): #handle collisions
        pass
    
    def draw(self): #draws the ball
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)

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

class GiantRightWall(Paddle): #A giant wall the ball bounces off for testing purposes before AI paddle is implemented
    def __init__(self, window, x, y, width, height, color):
        super().__init__(window, x, y, width, height, color)
        self.rect = pygame.Rect(x, y, width, height)
    
    def move(self):
        pass
    
    def handle_event(self, event):
        pass

class regularBall(Ball):
    def __init__(self, window, x, y, radius, color):
        super().__init__(window, x, y, radius, color)
        self.rect = pygame.Rect(x, y, radius, radius)
        
    def move(self): #moves the ball
        self.x += self.dx
        self.y += self.dy
        # update rect
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.y <= 0 or self.y >= WINDOW_HEIGHT:
            self.dy *= -1
        if self.x <= 0:
            self.dx *= -1
        
    def handle_event(self, event): #handle collisions
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(GiantRightWall.rect):
            self.dx *= -1
            print("Collision detected")

# Game Elements
player_paddle = PlayerPaddle(window, 50, 50, 20, 100, (0, 0, 0))
ball = regularBall(window, 400, 300, 10, (0, 0, 0))
GiantRightWall = GiantRightWall(window, 750, 0, 50, 600, (0, 0, 0))

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
        
        GiantRightWall.draw()
        
        ball.move()
        ball.draw()
        # Game event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if exit_button.handleEvent(event):
                run = False
            ball.handle_event(event)
                
            
    pygame.display.update()