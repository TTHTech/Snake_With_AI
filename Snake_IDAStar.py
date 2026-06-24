import sys
import math
from pygame.math import Vector2

cell_size = 20
cell_number = 40
sys.setrecursionlimit(10000)


class Snake_IDAStar:
    """IDA*: lặp sâu dần theo ngưỡng f = g + h (Manhattan).
    Có giới hạn số nút (node_cap) + fallback tham lam để không bao giờ treo game."""

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def ida_star(snake, fruit, obstacles, node_cap=5000):
        start = tuple(snake.body[0])
        goal = tuple(fruit.pos)
        body_set = {tuple(b) for b in snake.body}
        obstacles_set = {tuple(obstacle.pos) for obstacle in obstacles}
        visited_cells = []

        if start == goal or goal in obstacles_set:
            return visited_cells, []

        counter = {'n': 0}
        best = {'h': Snake_IDAStar.heuristic(start, goal), 'path': [start]}

        def neighbors(cell):
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = cell[0] + dx, cell[1] + dy
                if (0 <= nx < cell_number and 0 <= ny < cell_number
                        and (nx, ny) not in body_set and (nx, ny) not in obstacles_set):
                    yield (nx, ny)

        def search(path_cells, g, threshold):
            node = path_cells[-1]
            counter['n'] += 1
            visited_cells.append(node)

            h = Snake_IDAStar.heuristic(node, goal)
            if h < best['h']:
                best['h'] = h
                best['path'] = list(path_cells)

            f = g + h
            if f > threshold:
                return f
            if node == goal:
                return 'FOUND'
            if counter['n'] > node_cap:
                return 'CAP'

            minimum = math.inf
            for nb in neighbors(node):
                if nb in path_cells:
                    continue
                path_cells.append(nb)
                t = search(path_cells, g + 1, threshold)
                if t == 'FOUND' or t == 'CAP':
                    return t
                if t < minimum:
                    minimum = t
                path_cells.pop()
            return minimum

        threshold = Snake_IDAStar.heuristic(start, goal)
        max_threshold = cell_number * cell_number
        result_cells = best['path']

        while True:
            path_cells = [start]
            t = search(path_cells, 0, threshold)
            if t == 'FOUND':
                result_cells = path_cells
                break
            if t == 'CAP' or t == math.inf or t > max_threshold:
                result_cells = best['path']  # fallback: tiến tới ô gần mồi nhất
                break
            threshold = t

        path = []
        for i in range(1, len(result_cells)):
            dx = result_cells[i][0] - result_cells[i - 1][0]
            dy = result_cells[i][1] - result_cells[i - 1][1]
            if (dx, dy) == (1, 0):
                path.append('RIGHT')
            elif (dx, dy) == (-1, 0):
                path.append('LEFT')
            elif (dx, dy) == (0, 1):
                path.append('DOWN')
            elif (dx, dy) == (0, -1):
                path.append('UP')
        return visited_cells, path

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
