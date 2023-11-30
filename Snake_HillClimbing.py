import pygame
from pygame.math import Vector2

cell_size = 20
cell_number = 40


class Snake_HillClimbing:

    def hill_climbing(snake, fruit, obstacles):
        start = tuple(snake.body[0])
        goal = tuple(fruit.pos)

        path = []
        current = start
        max_steps = cell_number * cell_number
        steps = 0


        obstacles_set = {tuple(obstacle.pos) for obstacle in obstacles}
        visited_cells = []

        while current != goal and steps < max_steps:
            neighbors = [
                (current[0], current[1] + 1), (current[0], current[1] - 1),
                (current[0] + 1, current[1]), (current[0] - 1, current[1])
            ]

            neighbors = [
                neighbor for neighbor in neighbors
                if 0 <= neighbor[0] < cell_number and 0 <= neighbor[1] < cell_number
                   and neighbor not in map(tuple, snake.body) and neighbor not in obstacles_set
            ]
            visited_cells.append(current)
            if not neighbors:
                break

            next_step = min(neighbors, key=lambda x: abs(goal[0] - x[0]) + abs(goal[1] - x[1]))

            if (next_step[0] - current[0], next_step[1] - current[1]) == (1, 0):
                path.append('RIGHT')
            elif (next_step[0] - current[0], next_step[1] - current[1]) == (-1, 0):
                path.append('LEFT')
            elif (next_step[0] - current[0], next_step[1] - current[1]) == (0, 1):
                path.append('DOWN')
            elif (next_step[0] - current[0], next_step[1] - current[1]) == (0, -1):
                path.append('UP')

            current = next_step
            steps += 1

        return visited_cells, path

    def follow_path(snake, path):
        if len(path) > 0:
            direction = path.pop(0)
            if direction == 'UP':
                snake.direction = Vector2(0, -1)
            elif direction == 'DOWN':
                snake.direction = Vector2(0, 1)
            elif direction == 'LEFT':
                snake.direction = Vector2(-1, 0)
            elif direction == 'RIGHT':
                snake.direction = Vector2(1, 0)

