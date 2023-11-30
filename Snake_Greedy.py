import sys
from pygame.math import Vector2
from queue import PriorityQueue
import snake

cell_size = 20
cell_number = 40
import math


class Snake_Greedy:
    def greedy(snake, fruit, obstacles):
        start = tuple(snake.body[0])
        goal = tuple(fruit.pos)

        frontier = PriorityQueue()
        frontier.put((Snake_Greedy.heuristic(start, goal), start))
        came_from = {start: None}
        obstacles_set = {tuple(obstacle.pos) for obstacle in obstacles}
        visited_cells = []

        while not frontier.empty():
            current = frontier.get()[1]
            visited_cells.append(current)

            if current == goal:
                break

            for next in [(current[0], current[1] + 1), (current[0], current[1] - 1), (current[0] + 1, current[1]),
                         (current[0] - 1, current[1])]:
                if 0 <= next[0] < cell_number and 0 <= next[1] < cell_number and next not in map(tuple, snake.body):
                    if next not in came_from and next not in obstacles_set:
                        priority = Snake_Greedy.heuristic(next, goal)
                        frontier.put((priority, next))
                        came_from[next] = current

        path = []
        while current != start:
            if (came_from[current][0] - current[0], came_from[current][1] - current[1]) == (1, 0):
                path.append('LEFT')
            elif (came_from[current][0] - current[0], came_from[current][1] - current[1]) == (-1, 0):
                path.append('RIGHT')
            elif (came_from[current][0] - current[0], came_from[current][1] - current[1]) == (0, 1):
                path.append('UP')
            elif (came_from[current][0] - current[0], came_from[current][1] - current[1]) == (0, -1):
                path.append('DOWN')
            current = came_from[current]

        return visited_cells, path[::-1]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

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
