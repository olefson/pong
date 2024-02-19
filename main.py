import pygame
import pygwidgets

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


# Buttons
start_button = pygwidgets.TextButton(window, (WINDOW_WIDTH / 2 - 100, 100), "Start Game")

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
        
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if start_button.handleEvent(event):
                    print("Start Game")
        pygame.display.update() 