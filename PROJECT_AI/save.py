import pygame, sys
from button import Button
from snake import *
from algotithm import *
cell_size = 40
cell_number = 20
class GameMenu:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
        pygame.display.set_caption("Snake")
        self.BG = pygame.image.load("assets/Background.png")

    def run(self):
        self.main_menu()

    def get_font(self, size):
        return pygame.font.Font("assets/font.ttf", size)
    def options(self):
        pass

    def play(self):
        main_game = MAIN()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    main_game.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)

            screen.fill((175, 215, 70))
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60)
    def main_menu(self):
        while True:
            self.SCREEN.blit(self.BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(70).render("S N A K E", True, "yellow")
            MENU_RECT = MENU_TEXT.get_rect(center=(430, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430,270 ),
                                 text_input="PLAY", font=self.get_font(75), base_color="yellow",
                                 hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 420),
                                    text_input="AI", font=self.get_font(75), base_color="yellow",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 570),
                                 text_input="QUIT", font=self.get_font(75), base_color="yellow",
                                 hovering_color="White")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


if __name__ == "__main__":
    game_menu = GameMenu()
    game_menu.run()
