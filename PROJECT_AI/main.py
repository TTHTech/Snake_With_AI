import pygame, sys
from button import Button
from snake import *
import Snake_UCS
import Snake_Dijikstra
# Initialize pygame and the screen
from Snake_BFS import *
pygame.init()
cell_size = 40
cell_number = 20
SCREEN = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption("Snake")
BG = pygame.image.load("assets/Background.png")
font = "assets/font.ttf"

def get_font(size):
    return pygame.font.Font(font, size)

def play():

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

def bfs_option():
    print("BFS Option Selected")
    main_game = MAIN()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SCREEN_UPDATE:
                main_game.update()
                path_to_food = main_game.Find_Path_BFS(main_game.fruit.pos)
                if path_to_food:
                    next_move = path_to_food[0] - main_game.snake.body[0]
                    main_game.snake.direction = Vector2(next_move.x, next_move.y)

        SCREEN.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def dfs_option():
    print("DFS Option Selected")

def ucs_option():
    print("UCS Option Selected")
def astar_option():
    print("A* Option Selected")

def greedy_option():
    print("Greedy Option Selected")

def dijkstra_option():
    print("Dijkstra's Option Selected")

def hillclimbing_option():
    print("Hill Climbing Option Selected")

# Mapping of options to functions
option_functions = {
    "BFS": bfs_option,
    "DFS": dfs_option,
    "UCS": ucs_option,
    "A.STAR": astar_option,
    "GREEDY": greedy_option,
    "DIJKSTRA": dijkstra_option,
    "HCB": hillclimbing_option,
}


def options():
    button_width = 200
    button_height = 50
    button_spacing = 90  # Khoảng cách giữa các nút

    # Tính toán khoảng cách từ mép trên của màn hình để nút đầu tiên có thể căn giữa
    total_buttons_height = (button_height * 4) + (button_spacing * 3)  # Cho 4 nút với 3 khoảng trống giữa
    start_y = (SCREEN.get_height() - total_buttons_height) // 2

    # Xác định vị trí cột của 2 hàng dọc
    left_column_x = SCREEN.get_width() // 4  # Cột bên trái ở 1/4 chiều rộng màn hình
    right_column_x = (SCREEN.get_width() * 3) // 4  # Cột bên phải ở 3/4 chiều rộng màn hình

    # Tạo các nút cho cột bên trái
    buttons_left = []
    option_texts_left = ["BFS", "DFS", "UCS", "A.STAR"]
    option_images_left = ["assets/button6.png"] * 4

    for i, (option_text, option_image) in enumerate(zip(option_texts_left, option_images_left)):
        button_pos_y = start_y + i * (button_height + button_spacing)
        button_image = pygame.image.load(option_image)
        buttons_left.append(Button(image=button_image, pos=(left_column_x, button_pos_y),
                              text_input=option_text, font=get_font(35), base_color="white", hovering_color="Green"))

    # Tạo các nút cho cột bên phải
    buttons_right = []
    option_texts_right = ["GREEDY", "DIJKSTRA", "HCB"]
    option_images_right = ["assets/button6.png"] * 3

    # Chỉ cần dùng start_y lại vì nó giữ nguyên vị trí y ban đầu
    for i, (option_text, option_image) in enumerate(zip(option_texts_right, option_images_right)):
        button_pos_y = start_y + i * (button_height + button_spacing)
        button_image = pygame.image.load(option_image)
        buttons_right.append(Button(image=button_image, pos=(right_column_x, button_pos_y),
                              text_input=option_text, font=get_font(35), base_color="white", hovering_color="Green"))

    # Gộp các nút từ cả hai cột vào một danh sách duy nhất để xử lý sự kiện
    buttons = buttons_left + buttons_right

    # Assume you have a 'BACK' button image as well
    back_button_image = pygame.image.load("assets/button6.png")
    button_pos_y += button_height + button_spacing
    buttons.append(Button(image=back_button_image, pos=(600, button_pos_y),
                          text_input="BACK", font=get_font(35), base_color="white", hovering_color="Green"))

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill((0, 0, 0))

        for button in buttons:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for index, button in enumerate(buttons):
                    if button.checkForInput(OPTIONS_MOUSE_POS):
                        # Check if index is in the range of the left buttons
                        if index < len(buttons_left):
                            option_selected = option_texts_left[index]
                            option_functions[option_selected]()  # Call the corresponding function
                        # Otherwise, it must be in the right buttons
                        elif index < len(buttons_left) + len(buttons_right):
                            # Adjust index for the right column
                            right_index = index - len(buttons_left)
                            option_selected = option_texts_right[right_index]
                            option_functions[option_selected]()  # Call the corresponding function
                        elif button == buttons[-1]:  # Assuming 'BACK' button is the last one added
                            main_menu()  # Go back to the main menu
                            return
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("S N A K E", True, "yellow")
        MENU_RECT = MENU_TEXT.get_rect(center=(430, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 270),
                             text_input="PLAY", font=get_font(75), base_color="yellow", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 420),
                                text_input="AI", font=get_font(75), base_color="yellow", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 570),
                             text_input="QUIT", font=get_font(75), base_color="yellow", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Run the main menu to start the game
main_menu()
