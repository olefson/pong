import pygame
import pygwidgets
from abc import ABC, abstractmethod

# Abstract Classes

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
        