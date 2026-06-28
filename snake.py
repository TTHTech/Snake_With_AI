import pygame, sys, random
from pygame.math import Vector2
import Snake_Dijikstra
import audio

# ===== Hệ thống SKIN cho rắn =====
# "Classic" = None -> dùng sprite gốc. Các skin khác được vẽ bằng code.
SKINS = {
    "Classic": None,
    "Emerald": {"body": (46, 204, 113), "body2": (33, 160, 90),  "head": (28, 130, 75),  "eye": (255, 255, 255), "pupil": (20, 45, 25)},
    "Ocean":   {"body": (52, 152, 219), "body2": (39, 118, 175), "head": (31, 97, 141),  "eye": (255, 255, 255), "pupil": (15, 35, 55)},
    "Lava":    {"body": (231, 96, 50),  "body2": (192, 64, 35),  "head": (150, 45, 30),  "eye": (255, 240, 200), "pupil": (70, 18, 12)},
    "Grape":   {"body": (155, 89, 182), "body2": (125, 60, 152), "head": (97, 45, 120),  "eye": (255, 255, 255), "pupil": (45, 22, 55)},
    "Gold":    {"body": (241, 196, 15), "body2": (210, 165, 12), "head": (170, 130, 8),  "eye": (60, 50, 10),    "pupil": (95, 72, 8)},
    "Shadow":  {"body": (52, 73, 94),   "body2": (40, 56, 72),   "head": (23, 32, 42),   "eye": (0, 255, 200),   "pupil": (8, 45, 38)},
}
selected_skin = "Classic"


def set_skin(name):
    global selected_skin
    if name in SKINS:
        selected_skin = name


# ===== Hệ thống MAP (chủ đề bàn cờ) =====
MAPS = {
    "Grass":  {"dark": (167, 227, 93),  "light": (196, 237, 100), "border": (56, 74, 12),   "inner": (120, 170, 60),  "obs": ("square",   (120, 120, 120))},
    "Desert": {"dark": (224, 196, 124), "light": (240, 218, 156), "border": (120, 88, 32),  "inner": (200, 160, 90),  "obs": ("triangle", (205, 165, 95))},
    "Ocean":  {"dark": (86, 158, 200),  "light": (120, 186, 222), "border": (28, 70, 104),  "inner": (150, 205, 235), "obs": ("diamond",  (40, 90, 130))},
    "Night":  {"dark": (42, 50, 74),    "light": (56, 66, 94),    "border": (16, 20, 34),   "inner": (90, 110, 150),  "obs": ("circle",   (150, 120, 205))},
    "Candy":  {"dark": (232, 150, 192), "light": (246, 182, 212), "border": (120, 48, 92),  "inner": (255, 210, 232), "obs": ("circle",   (235, 110, 170))},
    "Lava":   {"dark": (70, 40, 36),    "light": (96, 52, 44),    "border": (30, 14, 12),   "inner": (210, 90, 40),   "obs": ("ember",    (80, 40, 36))},
}
selected_map = "Grass"


def set_map(name):
    global selected_map
    if name in MAPS:
        selected_map = name


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10),
                     Vector2(3, 10)]  # mục đích tọa độ này là để cho thân ở bân trái đầu
        self.direction = Vector2(0, 0)
        self.new_block = False
        # tất cả vị trí đầu có thể có
        self.head_up = pygame.image.load('Graphics/head_up_s.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down_s.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right_s.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left_s.png').convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up, (20, 20))
        self.head_down = pygame.transform.scale(self.head_down, (20, 20))
        self.head_right = pygame.transform.scale(self.head_right, (20, 20))
        self.head_left = pygame.transform.scale(self.head_left, (20, 20))
        # tất cả vị trí đuôi có thể có
        self.tail_up = pygame.image.load('Graphics/tail_up_s.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down_s.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right_s.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left_s.png').convert_alpha()

        self.tail_up = pygame.transform.scale(self.tail_up, (20, 20))
        self.tail_down = pygame.transform.scale(self.tail_down, (20, 20))
        self.tail_right = pygame.transform.scale(self.tail_right, (20, 20))
        self.tail_left = pygame.transform.scale(self.tail_left, (20, 20))
        # 1 phần chiều dọc và 1 phần nằm ngang
        self.body_vertical = pygame.image.load('Graphics/body_vertical_s.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal_s.png').convert_alpha()

        self.body_vertical = pygame.transform.scale(self.body_vertical, (20, 20))
        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (20, 20))
        # các bộ phận cong của con rắn
        self.body_tr = pygame.image.load('Graphics/body_tr_s.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl_s.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br_s.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl_s.png').convert_alpha()

        # ====
        self.body_tr = pygame.transform.scale(self.body_tr, (20, 20))
        self.body_tl = pygame.transform.scale(self.body_tl, (20, 20))
        self.body_br = pygame.transform.scale(self.body_br, (20, 20))
        self.body_bl = pygame.transform.scale(self.body_bl, (20, 20))
        # self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')


    def draw_snake(self):
        if selected_skin != "Classic":
            self.draw_snake_skin(SKINS[selected_skin])
            return
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # tạo hình chữ nhật tại vị trí mà chúng ta cần nó
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def draw_snake_skin(self, palette):
        n = len(self.body)
        body, body2 = palette["body"], palette["body2"]
        for index, block in enumerate(self.body):
            rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            if index == 0:
                self.draw_head_skin(rect, palette)
                continue
            # Gradient từ đầu (body) tới đuôi (body2) -> đổi màu theo độ dài
            t = index / max(1, n - 1)
            col = (int(body[0] + (body2[0] - body[0]) * t),
                   int(body[1] + (body2[1] - body[1]) * t),
                   int(body[2] + (body2[2] - body[2]) * t))
            inner = tuple(max(0, c - 30) for c in col)
            pygame.draw.rect(screen, col, rect.inflate(-2, -2), border_radius=7)
            pygame.draw.rect(screen, inner, rect.inflate(-9, -9), border_radius=4)

    def draw_head_skin(self, rect, palette):
        pygame.draw.rect(screen, palette["head"], rect.inflate(-1, -1), border_radius=8)
        # Hướng đầu rắn để đặt mắt
        if len(self.body) >= 2:
            facing = self.body[0] - self.body[1]
        else:
            facing = Vector2(1, 0)
        fx, fy = int(facing.x), int(facing.y)
        cx, cy = rect.center
        off = int(cell_size * 0.22)
        eye_r = max(2, cell_size // 6)
        pupil_r = max(1, cell_size // 14)
        if fx != 0:
            eyes = [(cx + fx * off, cy - off), (cx + fx * off, cy + off)]
        else:
            eyes = [(cx - off, cy + fy * off), (cx + off, cy + fy * off)]
        for ex, ey in eyes:
            pygame.draw.circle(screen, palette["eye"], (ex, ey), eye_r)
            pygame.draw.circle(screen, palette["pupil"], (ex + fx * 2, ey + fy * 2), pupil_r)

    def update_head_graphics(self):

        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):

        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    # def play_crunch_sound(self):
    #     self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self, obstacles_positions):
        self.obstacles_positions = obstacles_positions
        self.randomize()

    def randomize(self):
        while True:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            if (self.x, self.y) not in self.obstacles_positions:
                self.pos = Vector2(self.x, self.y)
                break
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)  #





class MAIN:
    def __init__(self, n_obstacles=0):
        self.snake = SNAKE()
        self.obstacles = [OBSTACLE() for _ in range(n_obstacles)]
        self.n_obstacles = n_obstacles
        # Lưu vị trí của chướng ngại vật
        obstacles_positions = [tuple(obstacle.pos) for obstacle in self.obstacles]

        self.fruit = FRUIT(obstacles_positions)

        self.GameOver = False
        self.GamePause = False
        self.path = []
        self.effects = []   # hiệu ứng chớp sáng + "+1" khi ăn mồi
        self.final_score = 0  # điểm đạt được, lưu trước khi rắn reset

        self.background_image = pygame.image.load('assets/Back.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (800, cell_number * cell_size))

    def reset_obstacles(self):
        self.obstacles = [OBSTACLE() for _ in range(self.n_obstacles)]
    def update_occupied_positions(self):
        self.occupied = {tuple(block) for block in self.snake.body}
        for obstacle in self.obstacles:
            self.occupied.add(tuple(obstacle.pos))

    def randomize_positions(self):

        while True:
            self.fruit.randomize()
            if tuple(self.fruit.pos) not in self.occupied:
                break


        for obstacle in self.obstacles:
            while True:
                obstacle.randomize()
                if tuple(obstacle.pos) not in self.occupied:
                    break

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.update_occupied_positions()
        if self.GameOver:
            self.randomize_positions()
        if any(obstacle.pos == self.snake.body[0] for obstacle in self.obstacles):
            self.game_over()
    def draw_elements(self):
        # Bỏ overlay ảnh nền để chủ đề MAP (bàn cờ) hiển thị
        # screen.blit(self.background_image, (0, 0))
        # self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        for obstacle in self.obstacles:
            obstacle.draw_obstacle()
        self.draw_effects()
        self.draw_score()

    def draw_effects(self):
        for fx in self.effects[:]:
            fx['age'] += 1
            age = fx['age']
            cx = int(fx['pos'].x * cell_size + cell_size // 2)
            cy = int(fx['pos'].y * cell_size + cell_size // 2)
            radius = cell_size // 2 + age * 2
            alpha = max(0, 180 - age * 9)
            if alpha > 0:
                surf = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 255, 180, alpha), (radius + 1, radius + 1), radius, 3)
                screen.blit(surf, (cx - radius - 1, cy - radius - 1))
            txt = game_font.render("+1", True, (255, 240, 120))
            txt.set_alpha(max(0, 255 - age * 12))
            screen.blit(txt, txt.get_rect(center=(cx, cy - age * 2)))
            if age > 20:
                self.effects.remove(fx)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:  # lúc con rắn ăn thức ăn(vị trí thức ăn và rắn trùng nhau)
            self.effects.append({'pos': Vector2(self.snake.body[0]), 'age': 0})
            audio.play_eat()
            self.fruit.randomize()  # thức ăn random đến chỗ mới
            self.snake.add_block()  # rắn thêm 1 block

        # for block in self.snake.body[1:]:
        #     if block == self.fruit.pos:
        #         self.fruit.randomize()

    def check_fail(self):

        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            self.GameOver = True

        for block in self.snake.body[1:]:
            if len(self.snake.body) == 3 and self.snake.body[0] == Vector2(5, 10) and self.snake.body[1] == Vector2(5,10) and self.snake.body[2] == Vector2(4, 10):
                self.snake.reset()
            elif self.snake.body[0] == block:
                self.final_score = len(self.snake.body) - 3
                self.snake.reset()
                self.GameOver = True

    def game_over(self):
        self.final_score = len(self.snake.body) - 3
        self.GameOver = True
        self.snake.reset()
        self.reset_obstacles()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        grass_cell_size = 20
        grass_cell_number = cell_number * (cell_size // grass_cell_size)

        for row in range(grass_cell_number):
            for col in range(grass_cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * grass_cell_size, row * grass_cell_size, grass_cell_size,
                                             grass_cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score = len(self.snake.body) - 3
        label_surf = game_font.render("Score:", True, (190, 215, 130))
        value_surf = game_font.render(str(score), True, (245, 250, 220))
        panel_x, panel_y = 14, 14
        pad, gap, h = 12, 8, 34
        w = pad * 2 + label_surf.get_width() + gap + value_surf.get_width()

        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(bg, (28, 45, 12, 190), bg.get_rect(), border_radius=10)
        pygame.draw.rect(bg, (167, 209, 61), bg.get_rect(), 2, border_radius=10)
        screen.blit(bg, (panel_x, panel_y))

        cy = panel_y + (h - label_surf.get_height()) // 2
        screen.blit(label_surf, (panel_x + pad, cy))
        screen.blit(value_surf, (panel_x + pad + label_surf.get_width() + gap, cy))



    def draw_board_with_border(self):
        theme = MAPS.get(selected_map, MAPS["Grass"])
        dark, light = theme["dark"], theme["light"]

        for row in range(cell_number):
            for col in range(cell_number):
                x0, y0 = col * cell_size, row * cell_size
                color = dark if (row + col) % 2 == 0 else light
                pygame.draw.rect(screen, color, pygame.Rect(x0, y0, cell_size, cell_size))

        # Viền đôi tạo chiều sâu: khung ngoài đậm + đường trong sáng
        full = pygame.Rect(0, 0, cell_number * cell_size, cell_number * cell_size)
        pygame.draw.rect(screen, theme["border"], full, 8)
        pygame.draw.rect(screen, theme["inner"], full.inflate(-8, -8), 3)

class OBSTACLE:
    def __init__(self):

        self.image = pygame.image.load('assets/stone.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.randomize()

    def draw_obstacle(self):
        theme = MAPS.get(selected_map, MAPS["Grass"])
        shape, color = theme["obs"]
        x = int(self.pos.x * cell_size)
        y = int(self.pos.y * cell_size)
        rect = pygame.Rect(x, y, cell_size, cell_size).inflate(-2, -2)
        dark = tuple(max(0, c - 55) for c in color)

        if shape == "square":
            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.rect(screen, dark, rect, 2, border_radius=4)
        elif shape == "circle":
            pygame.draw.circle(screen, color, rect.center, rect.width // 2)
            pygame.draw.circle(screen, dark, rect.center, rect.width // 2, 2)
        elif shape == "triangle":
            pts = [(rect.centerx, rect.top), (rect.left, rect.bottom), (rect.right, rect.bottom)]
            pygame.draw.polygon(screen, color, pts)
            pygame.draw.polygon(screen, dark, pts, 2)
        elif shape == "diamond":
            pts = [(rect.centerx, rect.top), (rect.right, rect.centery),
                   (rect.centerx, rect.bottom), (rect.left, rect.centery)]
            pygame.draw.polygon(screen, color, pts)
            pygame.draw.polygon(screen, dark, pts, 2)
        elif shape == "ember":
            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.circle(screen, (240, 120, 40), rect.center, rect.width // 4)
            pygame.draw.rect(screen, (20, 10, 8), rect, 2, border_radius=4)
    def randomize(self):
        snake_start_positions = [(5, 10), (4, 10), (3, 10)]  # Vị trí bắt đầu cố định của rắn
        while True:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            if (self.x, self.y) not in snake_start_positions:
                self.pos = Vector2(self.x, self.y)
                break

# MENU=================================================================
# ===============================================================================
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 20
cell_number = 40
screen = pygame.display.set_mode((1200, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('assets/diamond.png').convert_alpha()
apple = pygame.transform.scale(apple, (20, 20))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 50)




