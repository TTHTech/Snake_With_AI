from button import Button
import pygame, sys
from button import Button
from snake import *

class DisplayMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load("assets/Background.png")  # Load background image
        self.menu_mouse_pos = None
        self.create_buttons()

    def get_font(size):
        return pygame.font.Font(font, size)
    def create_buttons(self):
        self.play_button = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 270),
                                  text_input="PLAY", font=get_font(75), base_color="yellow", hovering_color="White")
        self.options_button = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 420),
                                     text_input="AI", font=get_font(75), base_color="yellow", hovering_color="White")
        self.quit_button = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 570),
                                  text_input="QUIT", font=get_font(75), base_color="yellow", hovering_color="White")

    def run(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            self.menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(70).render("S N A K E", True, "yellow")
            menu_rect = menu_text.get_rect(center=(430, 100))
            self.screen.blit(menu_text, menu_rect)

            for button in [self.play_button, self.options_button, self.quit_button]:
                button.changeColor(self.menu_mouse_pos)
                button.update(self.screen)

            self.handle_events()
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(self.menu_mouse_pos):
                    pass
                elif self.options_button.checkForInput(self.menu_mouse_pos):
                    pass
                elif self.quit_button.checkForInput(self.menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((Your_Screen_Width, Your_Screen_Height))

# Create a MainMenu instance
display = DisplayMenu(screen)

# Run the main menu
display.run()
