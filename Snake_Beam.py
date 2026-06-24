from pygame.math import Vector2

cell_size = 20
cell_number = 40


class Snake_Beam:
    """Beam Search: như BFS nhưng mỗi lớp chỉ giữ lại `beam_width` nút tốt nhất theo heuristic."""

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(cell, body_set, obstacles_set):
        result = []
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = cell[0] + dx, cell[1] + dy
            if (0 <= nx < cell_number and 0 <= ny < cell_number
                    and (nx, ny) not in body_set and (nx, ny) not in obstacles_set):
                result.append((nx, ny))
        return result

    def beam_search(snake, fruit, obstacles, beam_width=20):
        start = tuple(snake.body[0])
        goal = tuple(fruit.pos)
        body_set = {tuple(b) for b in snake.body}
        obstacles_set = {tuple(obstacle.pos) for obstacle in obstacles}
        visited_cells = []

        came_from = {start: None}
        frontier = [start]
        found = False
        steps = 0
        max_steps = cell_number * cell_number

        while frontier and not found and steps < max_steps:
            steps += 1
            candidates = []
            for current in frontier:
                visited_cells.append(current)
                if current == goal:
                    found = True
                    break
                for nb in Snake_Beam.neighbors(current, body_set, obstacles_set):
                    if nb not in came_from:
                        came_from[nb] = current
                        candidates.append(nb)
            if found:
                break
            # Chỉ giữ beam_width ứng viên gần mồi nhất
            candidates.sort(key=lambda c: Snake_Beam.heuristic(c, goal))
            frontier = candidates[:beam_width]

        if goal not in came_from:
            return visited_cells, []

        cells = []
        node = goal
        while node is not None:
            cells.append(node)
            node = came_from[node]
        cells.reverse()

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
