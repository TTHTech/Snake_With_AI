import pygame, sys, random
from pygame.math import Vector2


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
        self.tail_left= pygame.transform.scale(self.tail_left, (20, 20))
        # 1 phần chiều dọc và 1 phần nằm ngang
        self.body_vertical = pygame.image.load('Graphics/body_vertical_s.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal_s.png').convert_alpha()

        self.body_vertical= pygame.transform.scale(self.body_vertical, (20, 20))
        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (20, 20))
        # các bộ phận cong của con rắn
        self.body_tr = pygame.image.load('Graphics/body_tr_s.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl_s.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br_s.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl_s.png').convert_alpha()

        #====
        self.body_tr = pygame.transform.scale(self.body_tr, (20, 20))
        self.body_tl = pygame.transform.scale(self.body_tl, (20, 20))
        self.body_br  = pygame.transform.scale(self.body_br , (20, 20))
        self.body_bl  = pygame.transform.scale(self.body_bl , (20, 20))
        # self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    # tổng cộng có 14 hình khác nhau
    def draw_snake(self):
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

    def update_head_graphics(self):
        # 1[4,10] body block at start - [5,10] Head pos at start = [-1,0] First block is to the left of the head
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
        # phần tử cuối cùng và phần tử đứng trước phần tử cuối cùng
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
            body_copy.insert(0, body_copy[0] + self.direction)  # thêm 1 vị trí mới ở phía trước để mở rộng con rắn
            self.body = body_copy[:]
            self.new_block = False  # đặt block mới là fail nếu không nó sẽ kéo dài mãi
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
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)  # vẽ 1 quả táo lên hình chữ nhật

    # pygame.draw.rect(screen,(126,166,114),fruit_rect) này vẽ hình chữ nhật

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:  # lúc con rắn ăn thức ăn(vị trí thức ăn và rắn trùng nhau)
            self.fruit.randomize()  # thức ăn random đến chỗ mới
            self.snake.add_block()  # rắn thêm 1 block
            # self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # kiểm tra xem con rắn có ở ngoài màn hình không
        # kiểm tra trái phải và trên dưới vì nó là 1 vector nên không thể so sánh với 1 số được
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()  # game sẽ kết thúc và bắt đầu lại
        # kiểm tra xem đầu con rắn có va chạm với bắt kì vị trí nào cuủa nó không
        # lấy tất cả các phần tử trừ đầu ra snake.body[1:]
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:  # đây kiểm tra có khối nào đụng đầu không snake.body[0]
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        grass_cell_size = 20  # Đặt kích thước ô cỏ nhỏ hơn so với cell_size gốc
        grass_cell_number = cell_number * (cell_size // grass_cell_size)  # Tính số lượng ô cỏ dựa trên kích thước mới

        for row in range(grass_cell_number):
            for col in range(grass_cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * grass_cell_size, row * grass_cell_size, grass_cell_size,
                                             grass_cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def Find_Path_BFS(self, food):
        queue = [(self.snake.body[0], [])]
        visited = set()
        while queue:
            current, path = queue.pop(0)
            if tuple(current) == tuple(food):  # Chuyển Vector2 thành tuple
                return path
            if tuple(current) in visited:  # Chuyển Vector2 thành tuple
                continue
            visited.add(tuple(current))  # Chuyển Vector2 thành tuple
            for move in [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]:
                next_position = current + move
                if (
                        0 <= next_position.x < cell_number
                        and 0 <= next_position.y < cell_number
                        and next_position not in self.snake.body
                ):
                    queue.append((next_position, path + [next_position]))



#===============================================================================
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 20
cell_number = 40
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png' ).convert_alpha()
apple = pygame.transform.scale(apple, (20, 20))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 10)
