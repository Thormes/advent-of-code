from collections import deque
from typing import Tuple, List, Dict

from utils.Grid import Grid


def aoc20():
    def find_path(start, end, grid) -> Tuple[int, List[Tuple[int, int]]]:
        queue = deque([(0, start, [start])])
        visited = set()
        steps = 0
        path: list[tuple[int, int]] = []
        while queue:
            steps, current_point, path = queue.pop()
            visited.add(current_point)
            if current_point == end:
                return steps, path

            for direction in directions:

                next_point = (current_point[0] + direction[0], current_point[1] + direction[1])
                x, y = next_point

                if 0 < x < grid.length and 0 < y < grid.width and grid.grid[x][y] in 'E.' and next_point not in visited:
                    queue.append((steps + 1, next_point, path + [next_point]))

        return steps, path

    def skips():
        economy = {}
        for cheat in skippable_walls:
            p1, p2 = cheat[1], cheat[2]
            ip1, ip2 = path.index(p1), path.index(p2)
            diff = abs(ip1 - ip2) - 2  # difference, removing start and endpoint of movement
            if not economy.get(diff, None):
                economy[diff] = 0
            economy[diff] += 1

        return economy

    def skips_by_length(max_length: int) -> Dict[int, int]:
        cheats = {}
        for idxp1, p1 in enumerate(path):
            for picos, p2 in enumerate(path[idxp1 + 1:]):
                distance = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])  # calculate Manhattan distance between path points
                time_saved = picos - distance + 1  # original distance minus shortest distance = economy
                if distance <= max_length and time_saved > 0:
                    if time_saved not in cheats:
                        cheats[time_saved] = 0
                    cheats[time_saved] += 1

        return cheats

    def partA():
        cheats = skips()
        count = 0
        for picoseconds, amount in cheats.items():
            if picoseconds >= 100:
                count += amount
        print(count)

    def partB():
        cheats = skips_by_length(20)
        count = 0
        for picoseconds, amount in cheats.items():
            if picoseconds >= 100:
                count += amount
        print(count)

    with (open('day20.input') as input_file):
        grid = Grid.from_str(input_file.read())
        # up, down, right, left
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        walls = []
        skippable_walls = []

        for x, row in enumerate(grid.grid):
            for y, cell in enumerate(row):
                if grid.grid[x][y] == 'S':
                    start = (x, y)
                if grid.grid[x][y] == 'E':
                    end = (x, y)
                if grid.grid[x][y] == '#':
                    walls.append((x, y))
                    if 0 < x - 1 < grid.length and 0 < x + 1 < grid.length and \
                            grid.grid[x - 1][y] in 'SE.' and grid.grid[x + 1][y] in 'SE.':
                        skippable_walls.append(((x, y), (x - 1, y), (x + 1, y)))
                    if 0 < y - 1 < grid.width and 0 < y + 1 < grid.width and \
                            grid.grid[x][y - 1] in 'SE.' and grid.grid[x][y + 1] in 'SE.':
                        skippable_walls.append(((x, y), (x, y - 1), (x, y + 1)))

        steps, path = find_path(start, end, grid)
        partA()
        partB()


aoc20()
