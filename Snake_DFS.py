from collections import deque
from pygame.math import Vector2

cell_size = 20
cell_number = 40

class Snake_DFS:


    def dfs(snake, food, obstacles):
        start = tuple(snake.body[0])
        goal = tuple(food.pos)

        stack = deque()
        stack.append(start)
        came_from = {start: None}
        visited = set()

        obstacles_set = {tuple(obstacle.pos) for obstacle in obstacles}

        while stack:
            current = stack.pop()
            visited.add(current)

            if current == goal:
                break

            for next in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                         (current[0], current[1] - 1), (current[0], current[1] + 1)]:
                if next not in came_from and next not in obstacles_set:
                    if 0 <= next[0] < cell_number and 0 <= next[1] < cell_number and next not in map(tuple, snake.body):
                        stack.appendleft(next)
                        came_from[next] = current

        path = []
        current = goal
        while current != start:
            if came_from[current][0] - current[0] == 1:
                path.append('LEFT')
            elif came_from[current][0] - current[0] == -1:
                path.append('RIGHT')
            elif came_from[current][1] - current[1] == 1:
                path.append('UP')
            elif came_from[current][1] - current[1] == -1:
                path.append('DOWN')
            current = came_from[current]
        return path[::-1], visited

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
