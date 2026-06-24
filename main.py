import pygame, sys
import math
import json
from button import Button
from snake import *
import snake
import audio
import Snake_UCS
import Snake_Dijikstra
import Snake_AStar
import Snake_HillClimbing
import Snake_Greedy
import Snake_DFS
# Initialize pygame and the screen
import Snake_BFS
import Snake_BiBFS
import Snake_Beam
import Snake_IDAStar
import os
import time

# Cho phép in tiếng Việt ra console Windows mà không bị UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

os.environ['SDL_VIDEO_CENTERED'] = '1'
current_mode = 'manual'
current_level = 'easy'
snake_speed = 50
snake_time = 0
snake_run = -1
pygame.init()
cell_size = 20
cell_number = 40
block = 0
SCREEN = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption("Snake")
BG = pygame.image.load("assets/BackGround_s1.png")
BG = pygame.transform.scale(BG, (cell_size * cell_number, cell_size * cell_number))

ov = pygame.image.load("assets/o.png")
ov = pygame.transform.scale(ov, (cell_size * cell_number, cell_size * cell_number))

se = pygame.image.load("assets/settin.jpg_large ")
se = pygame.transform.scale(se, (cell_size * cell_number, cell_size * cell_number))

lev = pygame.image.load("assets/levv.jpg")
lev = pygame.transform.scale(lev, (cell_size * cell_number, cell_size * cell_number))

pau = pygame.image.load("assets/paus.jpg")
pau = pygame.transform.scale(pau, (cell_size * cell_number, cell_size * cell_number))

spe = pygame.image.load("assets/speed.png")
spe = pygame.transform.scale(spe, (cell_size * cell_number, cell_size * cell_number))

bav = pygame.image.load("assets/bav.jpg")
bav = pygame.transform.scale(bav, (cell_size * cell_number, cell_size * cell_number))

ag = pygame.image.load("assets/ag.jpg")
ag = pygame.transform.scale(ag, (cell_size * cell_number, cell_size * cell_number))
font = "Font/PoetsenOne-Regular.ttf"
n_obstacles = 0

def get_font(size):
    return pygame.font.Font(font, size)


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


def save_config():
    try:
        data = {
            'skin': snake.selected_skin,
            'map': snake.selected_map,
            'speed': snake_speed,
            'level': current_level,
            'sound': audio.sound_enabled,
        }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Config save error:", e)


def load_config():
    global snake_speed, current_level, n_obstacles
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    except Exception as e:
        print("Config load error:", e)
        return
    snake.set_skin(data.get('skin', 'Classic'))
    snake.set_map(data.get('map', 'Grass'))
    snake_speed = int(data.get('speed', snake_speed))
    current_level = data.get('level', current_level)
    n_obstacles = {'easy': 0, 'medium': 50, 'hard': 100}.get(current_level, 0)
    audio.sound_enabled = bool(data.get('sound', True))


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
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int(0)
    block = int(0)
    start_time = time.time()
    while True:
        snake_run += 1
        # Cập nhật lời gọi hàm bfs để bao gồm các chướng ngại vật
        path_to_fruit_view, path_to_fruit = Snake_BFS.Snake_BFS.bfs(main_game.snake, main_game.fruit,
                                                                    main_game.obstacles)
        Snake_BFS.Snake_BFS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)
        # Xử lý sự kiện
        if handle_events(main_game):
            break

        # Cập nhật và vẽ game
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        print("số nút là ", snake_run)
        save_to_file()
        # pygame.display.update()
        clock.tick(144)


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
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    start_time = time.time()
    path_to_fruit_view0 = []
    sk = int(0)
    block = int(0)
    while True:
        snake_run += 1

        path_to_fruit, visited = Snake_DFS.Snake_DFS.dfs(main_game.snake, main_game.fruit, main_game.obstacles)
        Snake_DFS.Snake_DFS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = visited
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(visited)

        if handle_events(main_game):
            break


        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        # pygame.display.update()
        clock.tick(144)



def ucs_option():
    print("UCS Option Selected")
    global current_mode
    current_mode = 'UCS'
    global n_obstacles
    global snake_speed
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    sk = int(0)
    block = int(0)
    path_to_fruit_view0 = []
    start_time = time.time()
    while True:
        snake_run += 1
        path_to_fruit_view, path_to_fruit = Snake_UCS.Snake_UCS.ucs(main_game.snake, main_game.fruit,
                                                                    main_game.obstacles)
        Snake_UCS.Snake_UCS.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)

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
            if main_game.GameOver:
                game_over()


        SCREEN.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        # pygame.display.update()
        clock.tick(144)


def astar_option():
    print("A* Option Selected")
    global current_mode
    current_mode = 'A.STAR'
    global n_obstacles
    global snake_speed
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int(0)
    block = int(0)
    start_time = time.time()
    while True:
        snake_run += 1
        path_to_fruit_view, path_to_fruit = Snake_AStar.Snake_AStar.a_star(main_game.snake, main_game.fruit,
                                                                           main_game.obstacles)
        Snake_AStar.Snake_AStar.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)
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
            if main_game.GameOver:
                game_over()
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        # pygame.display.update()
        clock.tick(144)


def greedy_option():
    print("Greedy Option Selected")
    global current_mode
    current_mode = 'GREEDY'
    global n_obstacles
    global snake_speed
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int(0)
    block = int(0)
    start_time = time.time()
    while True:
        snake_run += 1
        path_to_fruit_view, path_to_fruit = Snake_Greedy.Snake_Greedy.greedy(main_game.snake, main_game.fruit,
                                                                             main_game.obstacles)
        Snake_Greedy.Snake_Greedy.follow_path(main_game.snake, path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)
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
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        # pygame.display.update()
        clock.tick(144)


def dijkstra_option():
    global current_mode
    current_mode = 'DIJKSTRA'
    global n_obstacles
    global snake_speed
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int(0)
    block = int(0)
    start_time = time.time()
    while True:
        snake_run += 1
        path_to_fruit_view, path_to_fruit = Snake_Dijikstra.Snake_Dijkstra.dijkstra(main_game.snake, main_game.fruit,
                                                                                    main_game.obstacles)
        Snake_Dijikstra.Snake_Dijkstra.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)

        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)
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
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        # pygame.display.update()
        clock.tick(144)


def hillclimbing_option():
    global current_mode
    current_mode = 'HCB'
    global n_obstacles
    global snake_speed
    global snake_time
    global snake_run
    global block
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    print("Hill Climbing Option Selected")
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = int(0)
    block = int(0)
    start_time = time.time()
    while True:
        snake_run += 1
        path_to_fruit_view, path_to_fruit = Snake_HillClimbing.Snake_HillClimbing.hill_climbing(main_game.snake,
                                                                                                main_game.fruit,
                                                                                                main_game.obstacles)
        Snake_HillClimbing.Snake_HillClimbing.follow_path(main_game.snake, path_to_fruit)
        print(path_to_fruit)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)
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
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        end_time = time.time()
        total_time = end_time - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        # pygame.display.update()
        clock.tick(144)


def _ai_loop(mode, search_fn):
    """Khung chạy chung cho các thuật toán AI mới (giống bfs_option)."""
    global current_mode, n_obstacles, snake_speed, snake_time, snake_run, block
    current_mode = mode
    pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
    main_game = MAIN(n_obstacles)
    path_to_fruit_view0 = []
    sk = 0
    block = 0
    start_time = time.time()
    while True:
        snake_run += 1
        path_to_fruit_view, path_to_fruit = search_fn(main_game.snake, main_game.fruit, main_game.obstacles)
        if sk == (len(main_game.snake.body) - 3):
            path_to_fruit_view0 = path_to_fruit_view
            sk += 1
        fruit_view(path_to_fruit_view0)
        block += len(path_to_fruit_view)
        if handle_events(main_game):
            break
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        draw_block(len(path_to_fruit_view0))
        draw_block_promax(block)
        total_time = time.time() - start_time
        snake_time = "{:.2f}".format(total_time)
        draw_time("{:.2f}".format(total_time))
        save_to_file()
        clock.tick(144)


def bibfs_option():
    print("Bidirectional BFS Option Selected")

    def fn(sk, fr, ob):
        view, path = Snake_BiBFS.Snake_BiBFS.bibfs(sk, fr, ob)
        Snake_BiBFS.Snake_BiBFS.follow_path(sk, path)
        return view, path

    _ai_loop('BIBFS', fn)


def beam_option():
    print("Beam Search Option Selected")

    def fn(sk, fr, ob):
        view, path = Snake_Beam.Snake_Beam.beam_search(sk, fr, ob)
        Snake_Beam.Snake_Beam.follow_path(sk, path)
        return view, path

    _ai_loop('BEAM', fn)


def idastar_option():
    print("IDA* Option Selected")

    def fn(sk, fr, ob):
        view, path = Snake_IDAStar.Snake_IDAStar.ida_star(sk, fr, ob)
        Snake_IDAStar.Snake_IDAStar.follow_path(sk, path)
        return view, path

    _ai_loop('IDA*', fn)


# Mapping of options to functions
option_functions = {
    "BFS": bfs_option,
    "DFS": dfs_option,
    "UCS": ucs_option,
    "A.STAR": astar_option,
    "GREEDY": greedy_option,
    "DIJKSTRA": dijkstra_option,
    "HCB": hillclimbing_option,
    "BIBFS": bibfs_option,
    "BEAM": beam_option,
    "IDA*": idastar_option,
}
def draw_text_with_shadow(text, font, color, center, shadow=(20, 30, 10), offset=3):
    """Vẽ chữ có đổ bóng để tiêu đề nổi bật hơn."""
    shadow_surf = font.render(text, True, shadow)
    SCREEN.blit(shadow_surf, shadow_surf.get_rect(center=(center[0] + offset, center[1] + offset)))
    text_surf = font.render(text, True, color)
    SCREEN.blit(text_surf, text_surf.get_rect(center=center))


def draw_stat(label, value, row, accent=(167, 209, 61)):
    """Vẽ 1 dòng thông tin (panel bo góc bán trong suốt) ở góc trên-trái."""
    panel_x = 14
    panel_y = 14 + row * 38
    label_surf = game_font.render(f"{label}:", True, (190, 215, 130))
    value_surf = game_font.render(str(value), True, (245, 250, 220))
    pad, gap, h = 12, 8, 34
    w = pad * 2 + label_surf.get_width() + gap + value_surf.get_width()

    bg = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(bg, (28, 45, 12, 190), bg.get_rect(), border_radius=10)
    pygame.draw.rect(bg, accent, bg.get_rect(), 2, border_radius=10)
    screen.blit(bg, (panel_x, panel_y))

    cy = panel_y + (h - label_surf.get_height()) // 2
    screen.blit(label_surf, (panel_x + pad, cy))
    screen.blit(value_surf, (panel_x + pad + label_surf.get_width() + gap, cy))


def draw_block(block):
    draw_stat("Path", block, 2)


def draw_block_promax(block):
    draw_stat("Nodes", block, 3)


def draw_time(time):
    draw_stat("Time", f"{time}s", 1)

def fruit_view(path_to_fruit_view):
    glow = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 240, 120, 110), (cell_size // 2, cell_size // 2), cell_size // 2)
    pygame.draw.circle(glow, (255, 255, 80, 220), (cell_size // 2, cell_size // 2), cell_size // 4)
    for coord in path_to_fruit_view:
        screen.blit(glow, (int(coord[0] * cell_size), int(coord[1] * cell_size)))
    pygame.display.update()


def fruit_run_view(path_to_fruit_view):
    for coord in path_to_fruit_view:
        pygame.draw.circle(screen, (0, 0, 255),
                           (int(coord[0] * cell_size + cell_size // 2), int(coord[1] * cell_size + cell_size // 2)),
                           cell_size // 4)
    pygame.display.update()


# ===================== NGHIÊN CỨU / BENCHMARK =====================
benchmark_results = []          # mỗi phần tử: dict số liệu 1 lần chạy
benchmark_selected = set()      # các thuật toán được tick chọn
bench_level = 'easy'
bench_speed = 50

_LEVEL_OBS = {'easy': 0, 'medium': 50, 'hard': 100}
_SPEED_CYCLE = [100, 50, 25, 12]


def _search_normalized(label, sk, fr, ob):
    """Trả về (visited_cells, path) thống nhất cho mọi thuật toán."""
    if label == "BFS":
        return Snake_BFS.Snake_BFS.bfs(sk, fr, ob)
    if label == "DFS":
        p, v = Snake_DFS.Snake_DFS.dfs(sk, fr, ob)   # DFS trả (path, visited)
        return v, p
    if label == "UCS":
        return Snake_UCS.Snake_UCS.ucs(sk, fr, ob)
    if label == "A.STAR":
        return Snake_AStar.Snake_AStar.a_star(sk, fr, ob)
    if label == "GREEDY":
        return Snake_Greedy.Snake_Greedy.greedy(sk, fr, ob)
    if label == "DIJKSTRA":
        return Snake_Dijikstra.Snake_Dijkstra.dijkstra(sk, fr, ob)
    if label == "HCB":
        return Snake_HillClimbing.Snake_HillClimbing.hill_climbing(sk, fr, ob)
    if label == "BIBFS":
        return Snake_BiBFS.Snake_BiBFS.bibfs(sk, fr, ob)
    if label == "BEAM":
        return Snake_Beam.Snake_Beam.beam_search(sk, fr, ob)
    if label == "IDA*":
        return Snake_IDAStar.Snake_IDAStar.ida_star(sk, fr, ob)
    return [], []


def _apply_dir(snake_obj, d):
    if d == 'UP':
        snake_obj.direction = Vector2(0, -1)
    elif d == 'DOWN':
        snake_obj.direction = Vector2(0, 1)
    elif d == 'LEFT':
        snake_obj.direction = Vector2(-1, 0)
    elif d == 'RIGHT':
        snake_obj.direction = Vector2(1, 0)


def _bench_fps(speed):
    return max(30, min(120, 1000 // max(1, speed)))


def run_one_benchmark(label, level_key, n_obs, speed, idx, total):
    """Chạy 1 ván cho 1 thuật toán đến khi rắn chết. Trả về dict số liệu."""
    main_game = MAIN(n_obs)
    main_game.snake.direction = Vector2(1, 0)
    steps = nodes = 0
    last_score = 0
    step_cap = 1200
    aborted = False
    paused = False
    pause_started = 0.0
    paused_total = 0.0
    last_visited = []
    t0 = time.time()
    fps = _bench_fps(speed)

    def _draw_frame():
        screen.fill((175, 215, 70))
        main_game.draw_board_with_border()
        main_game.draw_elements()
        fruit_view(last_visited)
        draw_text_with_shadow(f"{label}   ({idx}/{total})", get_font(34), (255, 222, 60),
                              (SCREEN.get_width() // 2, 24))
        info = get_font(18).render(
            f"Lv:{level_key}  Score:{last_score}  Steps:{steps}  FPS:{fps}   "
            f"[SPACE]Pause [UP/DOWN]Speed [ESC]Skip", True, (245, 250, 220))
        SCREEN.blit(info, info.get_rect(center=(SCREEN.get_width() // 2, 54)))
        if paused:
            ov_s = pygame.Surface((SCREEN.get_width(), SCREEN.get_height()), pygame.SRCALPHA)
            ov_s.fill((0, 0, 0, 120))
            SCREEN.blit(ov_s, (0, 0))
            draw_text_with_shadow("PAUSED", get_font(64), (255, 222, 60), (SCREEN.get_width() // 2, 380))

    while not main_game.GameOver and steps < step_cap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    aborted = True
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pause_started = time.time()
                    else:
                        paused_total += time.time() - pause_started
                elif event.key in (pygame.K_UP, pygame.K_PLUS, pygame.K_EQUALS):
                    fps = min(120, fps + 10)
                elif event.key in (pygame.K_DOWN, pygame.K_MINUS):
                    fps = max(5, fps - 10)
        if aborted:
            break
        if paused:
            _draw_frame()
            pygame.display.update()
            clock.tick(30)
            continue

        visited, path = _search_normalized(label, main_game.snake, main_game.fruit, main_game.obstacles)
        last_visited = visited
        nodes += len(visited)
        if path:
            _apply_dir(main_game.snake, path[0])

        last_score = len(main_game.snake.body) - 3
        main_game.update()
        steps += 1

        _draw_frame()
        pygame.display.update()
        clock.tick(fps)

    elapsed = time.time() - t0 - paused_total
    return {
        'algo': label, 'level': level_key, 'speed': speed,
        'score': last_score, 'steps': steps, 'nodes': nodes,
        'time': round(elapsed, 2), 'nps': round(nodes / max(1, steps), 1),
        'capped': steps >= step_cap, 'aborted': aborted,
    }


def save_benchmark_csv():
    import csv
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark_results.csv')
    try:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['Algorithm', 'Level', 'Speed', 'Score', 'Steps', 'Nodes', 'Time(s)', 'Nodes/Step', 'Capped'])
            for r in benchmark_results:
                w.writerow([r['algo'], r['level'], r['speed'], r['score'], r['steps'],
                            r['nodes'], r['time'], r['nps'], r['capped']])
    except Exception as e:
        print("CSV save error:", e)


def run_benchmark(selected, level_key, speed):
    order = [a for a in option_functions.keys() if a in selected]
    n_obs = _LEVEL_OBS.get(level_key, 0)
    for idx, label in enumerate(order):
        res = run_one_benchmark(label, level_key, n_obs, speed, idx + 1, len(order))
        benchmark_results.append(res)
    save_benchmark_csv()
    benchmark_report()


def draw_toggle(rect, label, mouse, checked):
    hover = rect.collidepoint(mouse)
    fill = (60, 92, 40) if (hover or checked) else (40, 60, 26)
    pygame.draw.rect(SCREEN, fill, rect, border_radius=10)
    pygame.draw.rect(SCREEN, (255, 215, 60) if checked else (90, 120, 60), rect, 3, border_radius=10)
    box = pygame.Rect(rect.x + 12, rect.centery - 12, 24, 24)
    pygame.draw.rect(SCREEN, (20, 30, 12), box, border_radius=5)
    pygame.draw.rect(SCREEN, (255, 215, 60) if checked else (120, 150, 90), box, 2, border_radius=5)
    if checked:
        pygame.draw.circle(SCREEN, (255, 215, 60), box.center, 6)
    txt = get_font(24).render(label, True, (240, 248, 220))
    SCREEN.blit(txt, txt.get_rect(midleft=(box.right + 12, rect.centery)))
    return hover


def show_benchmark_charts():
    """Mở cửa sổ matplotlib so sánh các thuật toán + lưu PNG. Lỗi không ảnh hưởng game."""
    if not benchmark_results:
        return
    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except Exception as e:
        print("matplotlib khong san sang:", e)
        return
    rows = benchmark_results
    labels = [f"{r['algo']}\n{r['level'][:3]}" for r in rows]
    metrics = [('Score (fruits)', 'score', 'tab:green'),
               ('Steps survived', 'steps', 'tab:blue'),
               ('Nodes expanded', 'nodes', 'tab:red'),
               ('Time (s)', 'time', 'tab:orange')]
    try:
        fig, axes = plt.subplots(2, 2, figsize=(12, 7))
        fig.suptitle('Snake AI - So sanh thuat toan', fontsize=14, fontweight='bold')
        for ax, (title, key, c) in zip(axes.flat, metrics):
            vals = [r[key] for r in rows]
            bars = ax.bar(range(len(rows)), vals, color=c)
            ax.set_title(title)
            ax.set_xticks(range(len(rows)))
            ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
            ax.grid(axis='y', alpha=0.3)
            ax.bar_label(bars, fontsize=7, padding=2)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark_chart.png')
        fig.savefig(out, dpi=120)
        print("Da luu bieu do:", out)
        plt.show()
        plt.close(fig)
    except Exception as e:
        print("Chart error:", e)


def benchmark_report():
    grad = make_gradient((20, 30, 46), (8, 12, 20))
    headers = ['Algo', 'Lvl', 'Spd', 'Score', 'Steps', 'Nodes', 'Time', 'N/Step']
    col_x = [36, 165, 230, 300, 390, 480, 600, 690]
    row_h = 34
    top = 150
    scroll = 0
    chart_rect = pygame.Rect(110, SCREEN.get_height() - 66, 180, 50)
    clear_rect = pygame.Rect(310, SCREEN.get_height() - 66, 180, 50)
    back_rect = pygame.Rect(510, SCREEN.get_height() - 66, 180, 50)

    while True:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("REPORT", get_font(56), (255, 222, 60), (SCREEN.get_width() // 2, 60))

        for h, x in zip(headers, col_x):
            SCREEN.blit(get_font(20).render(h, True, (255, 215, 60)), (x, top - 36))
        pygame.draw.line(SCREEN, (120, 150, 90), (30, top - 6), (770, top - 6), 2)

        visible = max(1, (SCREEN.get_height() - top - 90) // row_h)
        best = max([r['score'] for r in benchmark_results], default=0)
        for i in range(scroll, min(len(benchmark_results), scroll + visible)):
            r = benchmark_results[i]
            y = top + (i - scroll) * row_h
            color = (120, 255, 120) if (r['score'] == best and best > 0) else (235, 245, 215)
            vals = [r['algo'], r['level'][:3], str(r['speed']), str(r['score']), str(r['steps']),
                    str(r['nodes']), str(r['time']), str(r['nps'])]
            for v, x in zip(vals, col_x):
                SCREEN.blit(get_font(19).render(v, True, color), (x, y))

        if not benchmark_results:
            s = get_font(28).render("Chua co du lieu - hay chay benchmark!", True, (200, 210, 180))
            SCREEN.blit(s, s.get_rect(center=(SCREEN.get_width() // 2, 320)))

        draw_menu_button(chart_rect, "Chart", MOUSE)
        draw_menu_button(clear_rect, "Clear", MOUSE)
        draw_menu_button(back_rect, "Back", MOUSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll = max(0, scroll - 1)
                elif event.button == 5:
                    scroll = min(max(0, len(benchmark_results) - visible), scroll + 1)
                elif chart_rect.collidepoint(MOUSE):
                    show_benchmark_charts()
                elif back_rect.collidepoint(MOUSE):
                    return
                elif clear_rect.collidepoint(MOUSE):
                    benchmark_results.clear()
                    scroll = 0
        pygame.display.update()


def benchmark_menu():
    global bench_level, bench_speed
    grad = make_gradient((20, 30, 46), (8, 12, 20))
    algos = list(option_functions.keys())
    col_w, row_h, gap_x, gap_y = 240, 52, 30, 14
    start_x = (SCREEN.get_width() - (2 * col_w + gap_x)) // 2
    start_y = 130
    toggles = []
    for i, name in enumerate(algos):
        c, r = i % 2, i // 2
        rect = pygame.Rect(start_x + c * (col_w + gap_x), start_y + r * (row_h + gap_y), col_w, row_h)
        toggles.append((rect, name))

    level_rect = pygame.Rect(150, 470, 240, 56)
    speed_rect = pygame.Rect(410, 470, 240, 56)
    start_rect = pygame.Rect(150, 540, 240, 56)
    report_rect = pygame.Rect(410, 540, 240, 56)
    clear_rect = pygame.Rect(150, 610, 240, 56)
    back_rect = pygame.Rect(410, 610, 240, 56)

    while True:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("RESEARCH", get_font(54), (255, 222, 60), (SCREEN.get_width() // 2, 60))
        sub = get_font(20).render("Tick chon thuat toan -> START (moi thuat toan chay 1 van den khi chet)",
                                  True, (200, 215, 175))
        SCREEN.blit(sub, sub.get_rect(center=(SCREEN.get_width() // 2, 100)))

        for rect, name in toggles:
            draw_toggle(rect, name, MOUSE, name in benchmark_selected)

        draw_menu_button(level_rect, f"Level: {bench_level}", MOUSE)
        draw_menu_button(speed_rect, f"Speed: {bench_speed}", MOUSE)
        draw_menu_button(start_rect, "START", MOUSE, selected=bool(benchmark_selected))
        draw_menu_button(report_rect, "REPORT", MOUSE)
        draw_menu_button(clear_rect, "CLEAR", MOUSE)
        draw_menu_button(back_rect, "BACK", MOUSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, name in toggles:
                    if rect.collidepoint(MOUSE):
                        if name in benchmark_selected:
                            benchmark_selected.discard(name)
                        else:
                            benchmark_selected.add(name)
                if level_rect.collidepoint(MOUSE):
                    keys = list(_LEVEL_OBS.keys())
                    bench_level = keys[(keys.index(bench_level) + 1) % len(keys)]
                elif speed_rect.collidepoint(MOUSE):
                    bench_speed = _SPEED_CYCLE[(_SPEED_CYCLE.index(bench_speed) + 1) % len(_SPEED_CYCLE)] \
                        if bench_speed in _SPEED_CYCLE else _SPEED_CYCLE[0]
                elif start_rect.collidepoint(MOUSE) and benchmark_selected:
                    run_benchmark(benchmark_selected, bench_level, bench_speed)
                elif report_rect.collidepoint(MOUSE):
                    benchmark_report()
                elif clear_rect.collidepoint(MOUSE):
                    benchmark_results.clear()
                elif back_rect.collidepoint(MOUSE):
                    main_menu()
                    return
        pygame.display.update()


def options():
    grad = make_gradient((24, 34, 52), (8, 12, 22))
    items = list(option_functions.keys()) + ["BACK"]
    cols = 3
    card_w, card_h, gap_x, gap_y = 205, 78, 22, 20
    total_w = cols * card_w + (cols - 1) * gap_x
    start_x = (SCREEN.get_width() - total_w) // 2
    start_y = 150
    cells = []
    for i, label in enumerate(items):
        r, c = divmod(i, cols)
        rect = pygame.Rect(start_x + c * (card_w + gap_x), start_y + r * (card_h + gap_y), card_w, card_h)
        cells.append((rect, label))

    while True:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("AI ALGORITHMS", get_font(50), (255, 222, 60), (SCREEN.get_width() // 2, 80))
        for rect, label in cells:
            draw_menu_button(rect, label, MOUSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, label in cells:
                    if rect.collidepoint(MOUSE):
                        if label == "BACK":
                            main_menu()
                            return
                        option_functions[label]()
        pygame.display.update()


def make_gradient(top_c, bot_c):
    """Tạo surface nền gradient dọc (dựng sẵn 1 lần)."""
    grad = pygame.Surface((SCREEN.get_width(), SCREEN.get_height()))
    h = grad.get_height()
    for y in range(h):
        t = y / h
        grad.fill((int(top_c[0] + (bot_c[0] - top_c[0]) * t),
                   int(top_c[1] + (bot_c[1] - top_c[1]) * t),
                   int(top_c[2] + (bot_c[2] - top_c[2]) * t)),
                  (0, y, grad.get_width(), 1))
    return grad


def draw_menu_button(rect, text, mouse, selected=False, subtitle=None):
    """Nút bo góc phẳng hiện đại; trả về True nếu đang hover."""
    hover = rect.collidepoint(mouse)
    fill = (66, 100, 44) if (hover or selected) else (44, 66, 28)
    pygame.draw.rect(SCREEN, fill, rect, border_radius=14)
    border = (255, 215, 60) if selected else ((150, 200, 90) if hover else (70, 95, 45))
    pygame.draw.rect(SCREEN, border, rect, 3, border_radius=14)
    color = (255, 222, 60) if selected else (240, 248, 220)
    if subtitle:
        main_s = get_font(34).render(text, True, color)
        SCREEN.blit(main_s, main_s.get_rect(center=(rect.centerx, rect.centery - 12)))
        sub_s = get_font(18).render(subtitle, True, (180, 205, 150))
        SCREEN.blit(sub_s, sub_s.get_rect(center=(rect.centerx, rect.centery + 18)))
    else:
        main_s = get_font(31).render(text, True, color)
        SCREEN.blit(main_s, main_s.get_rect(center=rect.center))
    if selected:
        pygame.draw.circle(SCREEN, (255, 215, 60), (rect.right - 24, rect.centery), 8)
        pygame.draw.circle(SCREEN, (40, 30, 0), (rect.right - 24, rect.centery), 8, 2)
    return hover


def speed_setting():
    global snake_speed
    presets = [("Slow", 100), ("Normal", 50), ("Fast", 25), ("Turbo", 12)]
    grad = make_gradient((26, 44, 18), (9, 16, 7))
    bw, bh, gap = 360, 72, 22
    x = (SCREEN.get_width() - bw) // 2
    start_y = 210
    rows = [(pygame.Rect(x, start_y + i * (bh + gap), bw, bh), lbl, val)
            for i, (lbl, val) in enumerate(presets)]
    back_rect = pygame.Rect(x, start_y + len(presets) * (bh + gap) + 8, bw, bh)

    running = True
    while running:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("SPEED", get_font(64), (255, 222, 60), (SCREEN.get_width() // 2, 110))
        for rect, lbl, val in rows:
            draw_menu_button(rect, lbl, MOUSE, selected=(snake_speed == val), subtitle=f"{val} ms/step")
        draw_menu_button(back_rect, "Back", MOUSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(MOUSE):
                    running = False
                for rect, lbl, val in rows:
                    if rect.collidepoint(MOUSE):
                        snake_speed = val
                        save_config()
                        print("Speed set to:", snake_speed)
        pygame.display.update()


def draw_skin_preview(card_rect, color):
    """Vẽ 1 con rắn mini xem trước trong thẻ skin."""
    seg, n = 26, 4
    total = n * seg
    x = card_rect.centerx - total // 2
    y = card_rect.top + 48
    darker = tuple(max(0, c - 45) for c in color)
    for i in range(n):
        r = pygame.Rect(x + i * seg, y, seg - 4, seg - 4)
        pygame.draw.rect(SCREEN, color if i % 2 == 0 else darker, r, border_radius=7)
    # Mắt trên đầu (segment phải nhất)
    hx = x + (n - 1) * seg + (seg - 4) // 2
    hy = y + (seg - 4) // 2
    for dy in (-5, 5):
        pygame.draw.circle(SCREEN, (255, 255, 255), (hx + 3, hy + dy), 3)
        pygame.draw.circle(SCREEN, (20, 20, 20), (hx + 4, hy + dy), 1)


def skin_menu():
    skins = list(snake.SKINS.keys())
    preview_colors = {name: (snake.SKINS[name]["body"] if snake.SKINS[name] else (70, 130, 180))
                      for name in skins}

    # Nền gradient dựng sẵn 1 lần
    grad = pygame.Surface((SCREEN.get_width(), SCREEN.get_height()))
    top_c, bot_c = (26, 44, 18), (9, 16, 7)
    for y in range(grad.get_height()):
        t = y / grad.get_height()
        grad.fill((int(top_c[0] + (bot_c[0] - top_c[0]) * t),
                   int(top_c[1] + (bot_c[1] - top_c[1]) * t),
                   int(top_c[2] + (bot_c[2] - top_c[2]) * t)),
                  (0, y, grad.get_width(), 1))

    cols = 3
    card_w, card_h, gap_x, gap_y = 200, 160, 30, 40
    start_x = (SCREEN.get_width() - (cols * card_w + (cols - 1) * gap_x)) // 2
    start_y = 180
    cards = []
    for i, name in enumerate(skins):
        r, c = divmod(i, cols)
        rect = pygame.Rect(start_x + c * (card_w + gap_x), start_y + r * (card_h + gap_y), card_w, card_h)
        cards.append((rect, name))

    BACK_BUTTON = Button(image=pygame.image.load("assets/button6.png"),
                         pos=(SCREEN.get_width() // 2, SCREEN.get_height() - 60),
                         text_input="Back", font=get_font(40), base_color="yellow", hovering_color="red")

    running = True
    while running:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("SKINS", get_font(70), (255, 222, 60), (SCREEN.get_width() // 2, 90))

        for rect, name in cards:
            is_selected = (name == snake.selected_skin)
            is_hover = rect.collidepoint(MOUSE)
            pygame.draw.rect(SCREEN, (38, 56, 24), rect, border_radius=14)
            border = (255, 215, 60) if is_selected else ((150, 200, 90) if is_hover else (70, 95, 45))
            pygame.draw.rect(SCREEN, border, rect, 4 if (is_selected or is_hover) else 2, border_radius=14)
            draw_skin_preview(rect, preview_colors[name])
            nm = get_font(26).render(name, True, (235, 245, 210))
            SCREEN.blit(nm, nm.get_rect(center=(rect.centerx, rect.bottom - 26)))
            if is_selected:
                pygame.draw.circle(SCREEN, (255, 215, 60), (rect.right - 18, rect.top + 18), 7)
                pygame.draw.circle(SCREEN, (40, 30, 0), (rect.right - 18, rect.top + 18), 7, 2)

        BACK_BUTTON.changeColor(MOUSE)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MOUSE):
                    running = False
                for rect, name in cards:
                    if rect.collidepoint(MOUSE):
                        snake.set_skin(name)
                        save_config()
        pygame.display.update()


def draw_map_preview(card_rect, theme):
    """Vẽ mini bàn cờ 4x4 theo chủ đề map trong thẻ."""
    n, cell = 4, 22
    total = n * cell
    x = card_rect.centerx - total // 2
    y = card_rect.top + 40
    for r in range(n):
        for c in range(n):
            color = theme["dark"] if (r + c) % 2 == 0 else theme["light"]
            pygame.draw.rect(SCREEN, color, pygame.Rect(x + c * cell, y + r * cell, cell, cell))
    pygame.draw.rect(SCREEN, theme["border"], pygame.Rect(x, y, total, total), 3)


def map_menu():
    maps = list(snake.MAPS.keys())
    grad = make_gradient((26, 44, 18), (9, 16, 7))
    cols = 3
    card_w, card_h, gap_x, gap_y = 200, 170, 30, 34
    start_x = (SCREEN.get_width() - (cols * card_w + (cols - 1) * gap_x)) // 2
    start_y = 170
    cards = []
    for i, name in enumerate(maps):
        r, c = divmod(i, cols)
        rect = pygame.Rect(start_x + c * (card_w + gap_x), start_y + r * (card_h + gap_y), card_w, card_h)
        cards.append((rect, name))
    back_rect = pygame.Rect((SCREEN.get_width() - 360) // 2, SCREEN.get_height() - 92, 360, 64)

    running = True
    while running:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("MAP", get_font(70), (255, 222, 60), (SCREEN.get_width() // 2, 90))

        for rect, name in cards:
            is_selected = (name == snake.selected_map)
            is_hover = rect.collidepoint(MOUSE)
            pygame.draw.rect(SCREEN, (38, 56, 24), rect, border_radius=14)
            border = (255, 215, 60) if is_selected else ((150, 200, 90) if is_hover else (70, 95, 45))
            pygame.draw.rect(SCREEN, border, rect, 4 if (is_selected or is_hover) else 2, border_radius=14)
            draw_map_preview(rect, snake.MAPS[name])
            nm = get_font(26).render(name, True, (235, 245, 210))
            SCREEN.blit(nm, nm.get_rect(center=(rect.centerx, rect.bottom - 24)))
            if is_selected:
                pygame.draw.circle(SCREEN, (255, 215, 60), (rect.right - 18, rect.top + 18), 7)
                pygame.draw.circle(SCREEN, (40, 30, 0), (rect.right - 18, rect.top + 18), 7, 2)

        draw_menu_button(back_rect, "Back", MOUSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(MOUSE):
                    running = False
                for rect, name in cards:
                    if rect.collidepoint(MOUSE):
                        snake.set_map(name)
                        save_config()
        pygame.display.update()


def settings():
    grad = make_gradient((26, 44, 18), (9, 16, 7))
    bw, bh, gap = 360, 70, 22
    x = (SCREEN.get_width() - bw) // 2
    start_y = 200
    items = ["Speed", "Level", "Map", "Skins", "Sound", "Back"]
    rects = [pygame.Rect(x, start_y + i * (bh + gap), bw, bh) for i in range(len(items))]

    running = True
    while running:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("SETTINGS", get_font(58), (255, 222, 60), (SCREEN.get_width() // 2, 90))
        for rect, label in zip(rects, items):
            text = f"Sound: {'On' if audio.sound_enabled else 'Off'}" if label == "Sound" else label
            draw_menu_button(rect, text, MOUSE, selected=(label == "Sound" and audio.sound_enabled))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, label in zip(rects, items):
                    if rect.collidepoint(MOUSE):
                        if label == "Speed":
                            speed_setting()
                        elif label == "Level":
                            level_menu()
                        elif label == "Map":
                            map_menu()
                        elif label == "Skins":
                            skin_menu()
                        elif label == "Sound":
                            audio.set_enabled(not audio.sound_enabled)
                            save_config()
                        elif label == "Back":
                            running = False
        pygame.display.update()


def new_game():
    global n_obstacles, snake_speed
    if current_level == 'easy':
        n_obstacles = 0
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
    levels = [("Easy", "easy", 0), ("Medium", "medium", 50), ("Hard", "hard", 100)]
    grad = make_gradient((26, 44, 18), (9, 16, 7))
    bw, bh, gap = 360, 84, 26
    x = (SCREEN.get_width() - bw) // 2
    start_y = 220
    rows = [(pygame.Rect(x, start_y + i * (bh + gap), bw, bh), lbl, key, obs)
            for i, (lbl, key, obs) in enumerate(levels)]
    back_rect = pygame.Rect(x, start_y + len(levels) * (bh + gap) + 10, bw, 70)

    running = True
    while running:
        SCREEN.blit(grad, (0, 0))
        MOUSE = pygame.mouse.get_pos()
        draw_text_with_shadow("LEVEL", get_font(64), (255, 222, 60), (SCREEN.get_width() // 2, 120))
        for rect, lbl, key, obs in rows:
            sub = "No obstacles" if obs == 0 else f"{obs} obstacles"
            draw_menu_button(rect, lbl, MOUSE, selected=(current_level == key), subtitle=sub)
        draw_menu_button(back_rect, "Back", MOUSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(MOUSE):
                    running = False
                for rect, lbl, key, obs in rows:
                    if rect.collidepoint(MOUSE):
                        current_level = key
                        n_obstacles = obs
                        save_config()
        pygame.display.update()


def pause_menu():
    paused = True

    while paused:
        SCREEN.blit(pau, (0, 0))
        PAUSE_MOUSE_POS = pygame.mouse.get_pos()

        PAUSE_TEXT = get_font(70).render("Paused", True, "yellow")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(400, 100))

        CONTINUE_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 250),
                                 text_input="Continue", font=get_font(40), base_color="yellow", hovering_color="red")
        NEW_GAME_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 400),
                                 text_input="New Game", font=get_font(40), base_color="yellow", hovering_color="red")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 550),
                                text_input="Setting", font=get_font(40), base_color="yellow", hovering_color="red")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 700),
                             text_input="Quit", font=get_font(40), base_color="yellow", hovering_color="red")

        draw_text_with_shadow("Paused", get_font(70), (255, 222, 60), (400, 100))

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
        SCREEN.blit(ov, (0, 0))
        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()

        GAME_OVER_TEXT = get_font(70).render("Game Over", True, "Red")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(400, 100))

        NEW_GAME_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 270),
                                 text_input="New Game", font=get_font(40), base_color="yellow", hovering_color="red")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 420),
                                text_input="Setting", font=get_font(40), base_color="yellow", hovering_color="red")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button6.png"), pos=(400, 570),
                             text_input="Quit", font=get_font(40), base_color="yellow", hovering_color="red")

        draw_text_with_shadow("Game Over", get_font(70), (235, 60, 50), (400, 100))

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
                    main_menu()
                    return

        pygame.display.update()


current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'Snake.txt')

def save_to_file():
    global snake_speed, snake_time, snake_run, current_mode, current_level
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Thuật toán: {current_mode}\n")
            file.write(f"Chế độ hiện tại: {current_level}\n")
            file.write(f"Tốc độ rắn: {snake_speed}\n")
            file.write(f"Tổng số nút: {block}\n")
            file.write(f"Thời gian chạy chương trình: {snake_time}\n")
            file.write(f"Số nút(chi phí): {snake_run}\n")
    except Exception as e:
        print(f"An error occurred: {e}")



def main_menu():
    global current_mode, current_level
    current_mode == 'manual'
    grad = make_gradient((30, 52, 24), (8, 14, 6))
    btn_img = pygame.transform.scale(pygame.image.load("assets/button6.png"), (320, 92))
    while True:
        SCREEN.blit(grad, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Tiêu đề động: nhún nhẹ + quầng sáng nhấp nháy
        t = pygame.time.get_ticks() / 1000.0
        bob = int(math.sin(t * 2.2) * 6)
        glow = pygame.Surface((540, 170), pygame.SRCALPHA)
        ga = int(55 + 35 * (0.5 + 0.5 * math.sin(t * 3)))
        pygame.draw.ellipse(glow, (255, 210, 60, ga), glow.get_rect())
        SCREEN.blit(glow, glow.get_rect(center=(400, 90 + bob)))
        draw_text_with_shadow("S N A K E", get_font(70), (255, 222, 60), (400, 90 + bob))

        PLAY_BUTTON = Button(image=btn_img, pos=(400, 250),
                             text_input="PLAY", font=get_font(46), base_color="yellow", hovering_color="red")
        OPTIONS_BUTTON = Button(image=btn_img, pos=(400, 365),
                                text_input="AI", font=get_font(46), base_color="yellow", hovering_color="red")
        RESEARCH_BUTTON = Button(image=btn_img, pos=(400, 480),
                                 text_input="RESEARCH", font=get_font(40), base_color="yellow", hovering_color="red")
        QUIT_BUTTON = Button(image=btn_img, pos=(400, 595),
                             text_input="QUIT", font=get_font(46), base_color="yellow", hovering_color="red")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, RESEARCH_BUTTON, QUIT_BUTTON]:
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
                elif RESEARCH_BUTTON.checkForInput(MENU_MOUSE_POS):
                    benchmark_menu()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


audio.init()
load_config()
if audio.sound_enabled:
    audio.start_music()
main_menu()
