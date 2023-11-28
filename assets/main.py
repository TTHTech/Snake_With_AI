import pygame, sys
from button import Button
from snake import *
import Snake_UCS
import Snake_Dijikstra
import Snake_AStar
import Snake_HillClimbing
import Snake_Greedy
import Snake_DFS
# Initialize pygame and the screen
import Snake_BFS
current_mode = 'manual'
current_level = 'easy'
snake_speed = 50
pygame.init()
cell_size = 20
cell_number = 40
SCREEN = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption("Snake")
BG = pygame.image.load("assets/BackGround_s1.png")
BG = pygame.transform.scale(BG, (cell_size * cell_number, cell_size * cell_number))
font = "assets/font.ttf"
n_obstacles = 0


def get_font(size):
    return pygame.font.Font(font, size)


def play():
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    global n_obstacles
    main_game = MAIN(n_obstacles)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if not main_game.GameOver:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_menu()
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
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_result = pause_menu()
                        if pause_result == "main_menu":
                            return

            if main_game.GameOver:
                game_over_result = game_over()  # Nhận trạng thái trả về từ game_over
                if game_over_result == "main_menu":
                    return
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()

        pygame.display.update()
        clock.tick(60)


def bfs_option():
    print("BFS Option Selected")
    global current_mode
    current_mode = 'BFS'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int (0)
    while True:
        # Cập nhật lời gọi hàm bfs để bao gồm các chướng ngại vật
        path_to_fruit_view, path_to_fruit = Snake_BFS.Snake_BFS.bfs(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_BFS.Snake_BFS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        # Xử lý sự kiện
        if handle_events(main_game):
            break

        # Cập nhật và vẽ game
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
        clock.tick(60)

def handle_events(main_game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if not main_game.GameOver and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                pause_menu()
        if main_game.GameOver:
            game_over()
            return True
    return False

def dfs_option():
    print("DFS Option Selected")
    global current_mode
    current_mode = 'DFS'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int (0)
    while True:
        # Cập nhật lời gọi hàm dfs để bao gồm các chướng ngại vật
        path_to_fruit, visited = Snake_DFS.Snake_DFS.dfs(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_DFS.Snake_DFS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = visited
            sk += 1
        fruit_view(path_to_fruit_view0)
        # Xử lý sự kiện tương tự như trong bfs_option
        if handle_events(main_game):
            break

        # Cập nhật và vẽ game giống như bfs_option
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
        clock.tick(60)


def ucs_option():
    print("UCS Option Selected")
    global current_mode
    current_mode = 'UCS'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)  # Sử dụng số lượng chướng ngại vật đã được thiết lập
    sk = int (0)
    path_to_fruit_view0 = []
    while True:
        # Cập nhật lời gọi hàm ucs để bao gồm các chướng ngại vật
        path_to_fruit_view, path_to_fruit = Snake_UCS.Snake_UCS.ucs(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_UCS.Snake_UCS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        # Xử lý sự kiện tương tự như trong bfs_option
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if not main_game.GameOver:  # Check for input only if the game is not over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_menu()
            if main_game.GameOver:
                game_over()

        # Cập nhật và vẽ game giống như bfs_option
        SCREEN.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
        clock.tick(60)

def astar_option():
    print("A* Option Selected")
    global current_mode
    current_mode = 'A.STAR'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int (0)
    while True:
        path_to_fruit_view, path_to_fruit = Snake_AStar.Snake_AStar.a_star(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_AStar.Snake_AStar.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if not main_game.GameOver:  # Check for input only if the game is not over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_menu()
            if main_game.GameOver:
                game_over()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
        clock.tick(60)


def greedy_option():
    print("Greedy Option Selected")
    global current_mode
    current_mode = 'GREEDY'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int (0)
    while True:
        path_to_fruit_view, path_to_fruit = Snake_Greedy.Snake_Greedy.greedy(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_Greedy.Snake_Greedy.follow_path(main_game.snake, path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        print(path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if not main_game.GameOver:  # Check for input only if the game is not over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_menu()
            if main_game.GameOver:
                game_over()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
        clock.tick(60)


def dijkstra_option():
    global current_mode
    current_mode = 'DIJKSTRA'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int (0)
    while True:
        path_to_fruit_view, path_to_fruit = Snake_Dijikstra.Snake_Dijkstra.dijkstra(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_Dijikstra.Snake_Dijkstra.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        # fruit_run_view( path_to_fruit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if not main_game.GameOver:  # Check for input only if the game is not over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_menu()
            if main_game.GameOver:
                game_over()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
        clock.tick(60)


def hillclimbing_option():
    global current_mode
    current_mode = 'HCB'
    global n_obstacles
    global snake_speed
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    print("Hill Climbing Option Selected")
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int (0)
    while True:
        path_to_fruit_view, path_to_fruit = Snake_HillClimbing.Snake_HillClimbing.hill_climbing(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_HillClimbing.Snake_HillClimbing.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if not main_game.GameOver:  # Check for input only if the game is not over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        pause_menu()
            if main_game.GameOver:
                game_over()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        # pygame.display.update()
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
def fruit_view(path_to_fruit_view):
    for coord in path_to_fruit_view:
        pygame.draw.circle(screen, (255, 255, 0), (int(coord[0]*cell_size + cell_size//2), int(coord[1]*cell_size + cell_size//2)), cell_size//4)
    pygame.display.update()
def fruit_run_view(path_to_fruit_view):
    for coord in path_to_fruit_view:
        pygame.draw.circle(screen, (0, 0, 255), (int(coord[0]*cell_size + cell_size//2), int(coord[1]*cell_size + cell_size//2)), cell_size//4)
    pygame.display.update()
    
    
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
                                   text_input=option_text, font=get_font(35), base_color="yellow",
                                   hovering_color="white"))

    # Tạo các nút cho cột bên phải
    buttons_right = []
    option_texts_right = ["GREEDY", "DIJKSTRA", "HCB"]
    option_images_right = ["assets/button6.png"] * 3

    # Chỉ cần dùng start_y lại vì nó giữ nguyên vị trí y ban đầu
    for i, (option_text, option_image) in enumerate(zip(option_texts_right, option_images_right)):
        button_pos_y = start_y + i * (button_height + button_spacing)
        button_image = pygame.image.load(option_image)
        buttons_right.append(Button(image=button_image, pos=(right_column_x, button_pos_y),
                                    text_input=option_text, font=get_font(35), base_color="yellow",
                                    hovering_color="white"))

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

def speed_setting():
    global snake_speed
    speed_setting_running = True
    speed_input = ""
    input_box = pygame.Rect(SCREEN.get_width() // 2 - 100, SCREEN.get_height() // 2 - 80, 200, 40)
    input_active = True

    BACK_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 40),
                         text_input="Back", font=get_font(40), base_color="yellow", hovering_color="White")

    while speed_setting_running:
        SCREEN.fill((0, 0, 0))  # Đặt màu nền
        SPEED_SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        BACK_BUTTON.changeColor(SPEED_SETTINGS_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SPEED_SETTINGS_MOUSE_POS):
                    speed_setting_running = False

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    try:
                        snake_speed = int(speed_input)
                        print("Speed set to:", snake_speed)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                elif event.key == pygame.K_BACKSPACE:
                    speed_input = speed_input[:-1]
                else:
                    speed_input += event.unicode

        pygame.draw.rect(SCREEN, (255, 255, 255), input_box)
        text_surface = get_font(30).render(speed_input, True, (0, 0, 0))
        SCREEN.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.update()


def settings():
    setting_running = True
    while setting_running:
        SCREEN.fill((0, 0, 0))
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        # Tạo các nút cho cài đặt
        SETTING_1_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 250),
                                  text_input="Speed", font=get_font(40), base_color="yellow", hovering_color="White")
        SETTING_2_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 400),
                                  text_input="Level", font=get_font(40), base_color="yellow", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 550),
                             text_input="Back", font=get_font(40), base_color="yellow", hovering_color="White")

        for button in [SETTING_1_BUTTON, SETTING_2_BUTTON, BACK_BUTTON]:
            button.changeColor(SETTINGS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTING_1_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    speed_setting()
                elif SETTING_2_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    level_menu()
                elif BACK_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    setting_running = False

        pygame.display.update()
def new_game():
    global n_obstacles, snake_speed
    if current_level == 'not':
        n_obstacles = 0
    elif current_level == 'easy':
        n_obstacles = 10
    elif current_level == 'medium':
        n_obstacles = 50
    elif current_level == 'hard':
        n_obstacles = 100
    else:
        n_obstacles = 0

    if current_mode == 'manual':
        play()
    elif current_mode == 'BFS':
        bfs_option()
    elif current_mode == 'DFS':
        dfs_option()
    elif current_mode == 'UCS':
        ucs_option()
    elif current_mode == 'A.STAR':
        astar_option()
    elif current_mode == 'GREEDY':
        greedy_option()
    elif current_mode == 'DIJKSTRA':
        dijkstra_option()
    elif current_mode == 'HCB':
        hillclimbing_option()



def level_menu():
    global n_obstacles, current_level
    level_running = True
    while level_running:
        SCREEN.fill((0, 0, 0))
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        # Tạo các nút cho màn hình level
        EASY_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 200),
                             text_input="Easy", font=get_font(40), base_color="yellow", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 350),
                               text_input="Medium", font=get_font(40), base_color="yellow", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 500),
                             text_input="Hard", font=get_font(40), base_color="yellow", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 650),
                             text_input="Back", font=get_font(40), base_color="yellow", hovering_color="White")

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(LEVEL_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    n_obstacles = 20
                    current_level = 'easy'
                    break
                elif MEDIUM_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    n_obstacles = 50
                    current_level = 'medium'
                    break
                elif HARD_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    n_obstacles = 100
                    current_level = 'hard'
                    break
                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    level_running = False

        pygame.display.update()

    if level_running:
        main_menu()
def pause_menu():
    paused = True

    while paused:
        SCREEN.fill((0, 0, 0))
        PAUSE_MOUSE_POS = pygame.mouse.get_pos()

        PAUSE_TEXT = get_font(70).render("Paused", True, "yellow")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(430, 100))

        CONTINUE_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 250),
                                 text_input="Continue", font=get_font(40), base_color="yellow", hovering_color="White")
        NEW_GAME_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 400),
                                 text_input="New Game", font=get_font(40), base_color="yellow", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 550),
                                text_input="Setting", font=get_font(40), base_color="yellow", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 700),
                             text_input="Quit", font=get_font(40), base_color="yellow", hovering_color="White")

        SCREEN.blit(PAUSE_TEXT, PAUSE_RECT)

        for button in [CONTINUE_BUTTON, NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(PAUSE_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                    paused = False
                elif NEW_GAME_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                    new_game()
                elif OPTIONS_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                    settings()
                elif QUIT_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                    main_menu()  # Gọi hàm main_menu() thay vì trả về "main_menu"
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    paused = False

        pygame.display.update()
    return "continue"


def game_over():
    while True:
        SCREEN.fill((0, 0, 0))
        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()

        GAME_OVER_TEXT = get_font(70).render("Game Over", True, "Red")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(430, 100))

        NEW_GAME_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 270),
                                 text_input="New Game", font=get_font(40), base_color="yellow", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 420),
                                text_input="Setting", font=get_font(40), base_color="yellow", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(430, 570),
                             text_input="Quit", font=get_font(40), base_color="yellow", hovering_color="White")

        SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

        for button in [NEW_GAME_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(GAME_OVER_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEW_GAME_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    new_game()
                elif OPTIONS_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    settings()
                elif QUIT_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    main_menu()  # Gọi hàm main_menu() thay vì trả về "main_menu"
                    return

        pygame.display.update()


def main_menu():
    global current_mode, current_level
    current_mode == 'manual'
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
                    current_mode = 'manual'
                    play()
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
