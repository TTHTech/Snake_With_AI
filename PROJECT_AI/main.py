import pygame, sys
from button import Button
from snake import *
import Snake_UCS
import Snake_Dijikstra
import Snake_AStar
import Snake_HillClimbing
# Initialize pygame and the screen
import Snake_BFS
pygame.init()
cell_size = 20
cell_number = 40
SCREEN = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption("Snake")
BG = pygame.image.load("assets/BackGround_s1.png")
BG = pygame.transform.scale(BG, (cell_size * cell_number, cell_size * cell_number))
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
        main_game.draw_board_with_border()
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def bfs_option():
    print("BFS Option Selected")
    print("A* Option Selected")
    main_game = MAIN()
    while True:
        path_to_fruit = Snake_BFS.Snake_BFS.bfs(main_game.snake, main_game.fruit)
        Snake_BFS.Snake_BFS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def dfs_option():
    print("DFS Option Selected")

def ucs_option():
    print("UCS Option Selected")
    print("A* Option Selected")
    main_game = MAIN()
    while True:
        path_to_fruit = Snake_UCS.Snake_UCS.ucs(main_game.snake, main_game.fruit)
        Snake_UCS.Snake_UCS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
def astar_option():
    print("A* Option Selected")
    main_game = MAIN()
    while True:
        path_to_fruit = Snake_AStar.Snake_AStar.a_star(main_game.snake, main_game.fruit)
        Snake_AStar.Snake_AStar.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

def greedy_option():
    print("Greedy Option Selected")

def dijkstra_option():
    main_game = MAIN()
    while True:
        path_to_fruit = Snake_Dijikstra.Snake_Dijkstra.dijkstra(main_game.snake, main_game.fruit)
        Snake_Dijikstra.Snake_Dijkstra.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)


def hillclimbing_option():
    print("Hill Climbing Option Selected")
    main_game = MAIN()
    while True:
        path_to_fruit = Snake_HillClimbing.Snake_HillClimbing.hill_climbing(main_game.snake, main_game.fruit)
        Snake_HillClimbing.Snake_HillClimbing.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
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
    options_bg = pygame.image.load("assets/BackGround_s1.png")
    options_bg = pygame.transform.scale(options_bg, (cell_size * cell_number, cell_size * cell_number))
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
                              text_input=option_text, font=get_font(35), base_color="yellow", hovering_color="white"))

    # Tạo các nút cho cột bên phải
    buttons_right = []
    option_texts_right = ["GREEDY", "DIJKSTRA", "HCB"]
    option_images_right = ["assets/button6.png"] * 3

    # Chỉ cần dùng start_y lại vì nó giữ nguyên vị trí y ban đầu
    for i, (option_text, option_image) in enumerate(zip(option_texts_right, option_images_right)):
        button_pos_y = start_y + i * (button_height + button_spacing)
        button_image = pygame.image.load(option_image)
        buttons_right.append(Button(image=button_image, pos=(right_column_x, button_pos_y),
                              text_input=option_text, font=get_font(35), base_color="yellow", hovering_color="white"))

    # Gộp các nút từ cả hai cột vào một danh sách duy nhất để xử lý sự kiện
    buttons = buttons_left + buttons_right

    # Assume you have a 'BACK' button image as well
    back_button_image = pygame.image.load("assets/button6.png")
    button_pos_y += button_height + button_spacing
    buttons.append(Button(image=back_button_image, pos=(600, button_pos_y),
                          text_input="BACK", font=get_font(35), base_color="yellow", hovering_color="white"))

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(options_bg, (0, 0))

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
