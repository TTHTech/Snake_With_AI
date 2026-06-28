"""Q-Learning cho Snake - rắn TỰ HỌC qua thử-sai (không dùng tìm đường).

State (11 bit): nguy hiểm thẳng/phải/trái, hướng hiện tại (4), mồi ở trái/phải/trên/dưới.
Action (3): 0=đi thẳng, 1=rẽ phải, 2=rẽ trái  (tránh quay đầu 180 độ).
Reward: ăn mồi +10, chết -10, lại gần mồi +1, ra xa -1.
Cập nhật: Q(s,a) += alpha * (reward + gamma * max(Q(s')) - Q(s,a)).
"""
import os
import json
import random
from pygame.math import Vector2

cell_number = 40
_QPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qtable.json')

# Siêu tham số
ALPHA = 0.1
GAMMA = 0.9

Q = {}            # state(str) -> [q_thang, q_phai, q_trai]
_loaded = False


def _turn_right(d):
    return Vector2(-d.y, d.x)


def _turn_left(d):
    return Vector2(d.y, -d.x)


def _danger(pt, body_set, obstacles_set):
    x, y = int(pt.x), int(pt.y)
    if not (0 <= x < cell_number and 0 <= y < cell_number):
        return True
    return (x, y) in body_set or (x, y) in obstacles_set


def get_state(snake_obj, fruit, obstacles):
    d = snake_obj.direction
    if d == Vector2(0, 0):
        d = Vector2(1, 0)
    head = snake_obj.body[0]
    body_set = {(int(b.x), int(b.y)) for b in snake_obj.body}
    obstacles_set = {(int(o.pos.x), int(o.pos.y)) for o in obstacles}
    rd, ld = _turn_right(d), _turn_left(d)
    fx, fy = fruit.pos.x, fruit.pos.y
    bits = (
        int(_danger(head + d, body_set, obstacles_set)),
        int(_danger(head + rd, body_set, obstacles_set)),
        int(_danger(head + ld, body_set, obstacles_set)),
        int(d == Vector2(-1, 0)), int(d == Vector2(1, 0)),
        int(d == Vector2(0, -1)), int(d == Vector2(0, 1)),
        int(fx < head.x), int(fx > head.x), int(fy < head.y), int(fy > head.y),
    )
    return ''.join(map(str, bits))


def _action_dirs(d):
    if d == Vector2(0, 0):
        d = Vector2(1, 0)
    return [d, _turn_right(d), _turn_left(d)]   # thẳng, phải, trái


def _dir_name(d):
    if d == Vector2(0, -1):
        return 'UP'
    if d == Vector2(0, 1):
        return 'DOWN'
    if d == Vector2(-1, 0):
        return 'LEFT'
    if d == Vector2(1, 0):
        return 'RIGHT'
    return 'RIGHT'


def load_q():
    global Q, _loaded
    try:
        with open(_QPATH, 'r', encoding='utf-8') as f:
            Q = json.load(f)
    except Exception:
        Q = {}
    _loaded = True


def save_q():
    try:
        with open(_QPATH, 'w', encoding='utf-8') as f:
            json.dump(Q, f)
    except Exception as e:
        print("Q save error:", e)


def train(episodes=5000, progress_cb=None, obstacles='mixed', eps_start=1.0):
    """Huấn luyện headless (học CỘNG DỒN vào bảng Q hiện có, không xóa).

    obstacles: 'mixed' (ngẫu nhiên 0..100) hoặc một số nguyên cố định.
    progress_cb(ep, episodes, avg, eps, best) trả False để dừng sớm.
    """
    global Q
    import snake as snk
    scores = []
    best = 0
    for ep in range(episodes):
        eps = max(0.01, eps_start * (1 - ep / (episodes * 0.8)))
        if obstacles == 'mixed':
            n_obs = random.choice([0, 0, 30, 50, 80, 100])
        else:
            n_obs = int(obstacles)
        game = snk.MAIN(n_obs)
        game.snake.direction = Vector2(1, 0)
        state = get_state(game.snake, game.fruit, game.obstacles)
        food_eaten = 0
        hunger = 0
        done = False
        while not done:
            dirs = _action_dirs(game.snake.direction)
            if random.random() < eps:
                a = random.randint(0, 2)
            else:
                qs = Q.get(state)
                a = max(range(3), key=lambda i: qs[i]) if qs else random.randint(0, 2)

            game.snake.direction = dirs[a]
            head = game.snake.body[0]
            food = game.fruit.pos
            new_head = head + game.snake.direction
            ate = int(new_head.x) == int(food.x) and int(new_head.y) == int(food.y)
            prev_dist = abs(head.x - food.x) + abs(head.y - food.y)

            game.update()
            hunger += 1
            done = game.GameOver

            if done:
                reward = -10.0
            elif ate:
                reward = 10.0
                food_eaten += 1
                hunger = 0
            else:
                nh = game.snake.body[0]
                nd = abs(nh.x - food.x) + abs(nh.y - food.y)
                reward = 1.0 if nd < prev_dist else -1.0

            if hunger > 200:          # rắn đi lòng vòng -> cắt ván
                done = True

            next_state = get_state(game.snake, game.fruit, game.obstacles)
            qsa = Q.setdefault(state, [0.0, 0.0, 0.0])
            nxt = 0.0 if done else max(Q.get(next_state, [0.0, 0.0, 0.0]))
            qsa[a] += ALPHA * (reward + GAMMA * nxt - qsa[a])
            state = next_state

        scores.append(food_eaten)
        best = max(best, food_eaten)
        if progress_cb and ep % 100 == 0:
            avg = sum(scores[-100:]) / min(len(scores), 100)
            if progress_cb(ep, episodes, avg, eps, best) is False:
                break
    save_q()
    return best


def best_action(snake_obj, fruit, obstacles):
    if not _loaded:
        load_q()
    state = get_state(snake_obj, fruit, obstacles)
    dirs = _action_dirs(snake_obj.direction)
    qs = Q.get(state)
    if qs is not None:
        a = max(range(3), key=lambda i: qs[i])
    else:
        # Trạng thái chưa học: chọn hành động không chết, ưu tiên đi thẳng
        body_set = {(int(b.x), int(b.y)) for b in snake_obj.body}
        obstacles_set = {(int(o.pos.x), int(o.pos.y)) for o in obstacles}
        head = snake_obj.body[0]
        a = 0
        for i in range(3):
            if not _danger(head + dirs[i], body_set, obstacles_set):
                a = i
                break
    return [], [_dir_name(dirs[a])]


def follow_path(snake_obj, path):
    if len(path) > 0:
        d = path[0]
        if d == 'UP':
            snake_obj.direction = Vector2(0, -1)
        elif d == 'DOWN':
            snake_obj.direction = Vector2(0, 1)
        elif d == 'LEFT':
            snake_obj.direction = Vector2(-1, 0)
        elif d == 'RIGHT':
            snake_obj.direction = Vector2(1, 0)
