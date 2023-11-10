
class BFS:
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