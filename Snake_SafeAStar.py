"""Safe A* (kiểu Hamiltonian an toàn) - rắn gần như không bao giờ chết.

Ý tưởng:
  1. Tìm đường A* tới mồi.
  2. MÔ PHỎNG đi theo đường đó; sau khi ăn, kiểm tra đầu rắn có còn đường
     về tới đuôi không (BFS). Nếu CÓ -> đi an toàn, lấy bước đầu.
  3. Nếu không an toàn -> ĐI THEO ĐUÔI (đường tới ô đuôi) để câu giờ chờ lối mở.
  4. Nếu vẫn bí -> chọn ô lân cận còn nhiều không gian trống nhất (flood fill).
"""
import heapq
from collections import deque
from pygame.math import Vector2

cell_size = 20
cell_number = 40

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Snake_SafeAStar:

    def _h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _in_bounds(c):
        return 0 <= c[0] < cell_number and 0 <= c[1] < cell_number

    def _astar(start, goal, blocked, visited_cells):
        openh = [(Snake_SafeAStar._h(start, goal), 0, start)]
        came = {start: None}
        gscore = {start: 0}
        while openh:
            _, g, cur = heapq.heappop(openh)
            visited_cells.append(cur)
            if cur == goal:
                path = []
                n = cur
                while n is not None:
                    path.append(n)
                    n = came[n]
                return path[::-1]
            for dx, dy in DIRS:
                nb = (cur[0] + dx, cur[1] + dy)
                if not Snake_SafeAStar._in_bounds(nb) or nb in blocked:
                    continue
                ng = g + 1
                if nb not in gscore or ng < gscore[nb]:
                    gscore[nb] = ng
                    came[nb] = cur
                    heapq.heappush(openh, (ng + Snake_SafeAStar._h(nb, goal), ng, nb))
        return None

    def _reachable(start, goal, blocked):
        if start == goal:
            return True
        q = deque([start])
        seen = {start}
        while q:
            cur = q.popleft()
            for dx, dy in DIRS:
                nb = (cur[0] + dx, cur[1] + dy)
                if nb == goal:
                    return True
                if Snake_SafeAStar._in_bounds(nb) and nb not in blocked and nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        return False

    def _flood_count(start, blocked):
        if not Snake_SafeAStar._in_bounds(start) or start in blocked:
            return 0
        q = deque([start])
        seen = {start}
        while q:
            cur = q.popleft()
            for dx, dy in DIRS:
                nb = (cur[0] + dx, cur[1] + dy)
                if Snake_SafeAStar._in_bounds(nb) and nb not in blocked and nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        return len(seen)

    def _simulate(body, path, food):
        nb = deque(body)
        for cell in path[1:]:
            nb.appendleft(cell)
            if cell != food:
                nb.pop()
        return list(nb)

    def _dir_name(dx, dy):
        if (dx, dy) == (1, 0):
            return 'RIGHT'
        if (dx, dy) == (-1, 0):
            return 'LEFT'
        if (dx, dy) == (0, 1):
            return 'DOWN'
        if (dx, dy) == (0, -1):
            return 'UP'
        return None

    def safe_a_star(snake, fruit, obstacles):
        body = [tuple(b) for b in snake.body]
        head, tail = body[0], body[-1]
        food = tuple(fruit.pos)
        obstacles_set = {tuple(o.pos) for o in obstacles}
        visited_cells = []
        chosen = None

        # 1) A* tới mồi (đuôi sẽ di chuyển nên không chặn ô đuôi)
        blocked_food = set(body[:-1]) | obstacles_set
        path = Snake_SafeAStar._astar(head, food, blocked_food, visited_cells)
        if path and len(path) >= 2:
            new_body = Snake_SafeAStar._simulate(body, path, food)
            nb_blocked = set(new_body[:-1]) | obstacles_set
            if Snake_SafeAStar._reachable(new_body[0], new_body[-1], nb_blocked):
                chosen = path[1]

        # 2) Không an toàn -> đi theo đuôi để câu giờ
        if chosen is None and len(body) > 1:
            blocked_tail = set(body[1:-1]) | obstacles_set
            tpath = Snake_SafeAStar._astar(head, tail, blocked_tail, visited_cells)
            if tpath and len(tpath) >= 2:
                chosen = tpath[1]

        # 3) Bí -> chọn ô lân cận còn nhiều không gian nhất
        if chosen is None:
            blocked_all = set(body) | obstacles_set
            best = -1
            for dx, dy in DIRS:
                nb = (head[0] + dx, head[1] + dy)
                if Snake_SafeAStar._in_bounds(nb) and nb not in blocked_all:
                    space = Snake_SafeAStar._flood_count(nb, set(body[:-1]) | obstacles_set)
                    if space > best:
                        best = space
                        chosen = nb

        if chosen is None:
            return visited_cells, []
        return visited_cells, [Snake_SafeAStar._dir_name(chosen[0] - head[0], chosen[1] - head[1])]

    def follow_path(snake, path):
        if len(path) > 0:
            direction = path[0]
            if direction == 'UP':
                snake.direction = Vector2(0, -1)
            elif direction == 'DOWN':
                snake.direction = Vector2(0, 1)
            elif direction == 'LEFT':
                snake.direction = Vector2(-1, 0)
            elif direction == 'RIGHT':
                snake.direction = Vector2(1, 0)
