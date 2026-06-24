from pygame.math import Vector2
from collections import deque

cell_size = 20
cell_number = 40


class Snake_BiBFS:
    """Bidirectional BFS: tìm đồng thời từ đầu rắn và từ mồi, gặp nhau ở giữa."""

    def neighbors(cell, body_set, obstacles_set):
        result = []
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = cell[0] + dx, cell[1] + dy
            if (0 <= nx < cell_number and 0 <= ny < cell_number
                    and (nx, ny) not in body_set and (nx, ny) not in obstacles_set):
                result.append((nx, ny))
        return result

    def bibfs(snake, fruit, obstacles):
        start = tuple(snake.body[0])
        goal = tuple(fruit.pos)
        body_set = {tuple(b) for b in snake.body}
        obstacles_set = {tuple(obstacle.pos) for obstacle in obstacles}
        visited_cells = []

        if start == goal or goal in obstacles_set:
            return visited_cells, []

        came_from_start = {start: None}
        came_from_goal = {goal: None}
        frontier_start = deque([start])
        frontier_goal = deque([goal])
        meeting = None

        while frontier_start and frontier_goal and meeting is None:
            # Mở rộng 1 lớp từ phía đầu rắn
            for _ in range(len(frontier_start)):
                current = frontier_start.popleft()
                visited_cells.append(current)
                if current in came_from_goal:
                    meeting = current
                    break
                for nb in Snake_BiBFS.neighbors(current, body_set, obstacles_set):
                    if nb not in came_from_start:
                        came_from_start[nb] = current
                        frontier_start.append(nb)
            if meeting is not None:
                break
            # Mở rộng 1 lớp từ phía mồi
            for _ in range(len(frontier_goal)):
                current = frontier_goal.popleft()
                visited_cells.append(current)
                if current in came_from_start:
                    meeting = current
                    break
                for nb in Snake_BiBFS.neighbors(current, body_set, obstacles_set):
                    if nb not in came_from_goal:
                        came_from_goal[nb] = current
                        frontier_goal.append(nb)

        if meeting is None:
            return visited_cells, []

        # start -> meeting
        forward = []
        node = meeting
        while node is not None:
            forward.append(node)
            node = came_from_start[node]
        forward.reverse()
        # meeting -> goal
        backward = []
        node = came_from_goal[meeting]
        while node is not None:
            backward.append(node)
            node = came_from_goal[node]

        cells = forward + backward

        path = []
        for i in range(1, len(cells)):
            dx = cells[i][0] - cells[i - 1][0]
            dy = cells[i][1] - cells[i - 1][1]
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
