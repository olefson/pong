import pygame
import pygwidgets
from abc import ABC, abstractmethod


# Abstract Classes
WINDOW_HEIGHT = 600

class Paddle(ABC): #abstract class for the paddles. To be used for the player and AI paddles
    def __init__(self, window, x, y, width, height, color):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    @abstractmethod
    def move(self): #moves up and down based on user input
        pass
    
    @abstractmethod
    def handle_event(self, event): #handles user input
        pass
    
    def collide_event_handler(self, event): #handles collisions
        steps = 10
        step_dy = 5/steps
        
        for i in range(steps):
            self.y += step_dy
            self.rect.y = self.y
            
            # check for window collision
            if self.y <= 0 or self.y + self.height >= WINDOW_HEIGHT:
                break

    def draw(self): #draws the paddle
        pygame.draw.rect(self.window, self.color, self.rect)


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
        