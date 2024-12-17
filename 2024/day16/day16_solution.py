import copy
import sys
from typing import Tuple, Set, List

from utils.Point import Point
from utils.Direction import Direction
from utils.Grid import Grid

sys.setrecursionlimit(10000)
import heapq

directions = [
    Direction('right', 0, 1),
    Direction('down', 1, 0),
    Direction('left', 0, -1),
    Direction('up', -1, 0),
]
for i in range(len(directions)):
    directions[i].next_direction = directions[(i + 1) % len(directions)]
    directions[i].previous_direction = directions[i - 1] if i > 0 else directions[len(directions) - 1]

start_direction = directions[0]


def get_data(filename) -> Grid:
    with open(filename) as text_input:
        grid = Grid.from_str(text_input.read())

    return grid


def get_start_end(grid: Grid) -> Tuple[Point, Point]:
    start, end = None, None
    for x, row in enumerate(grid.grid):
        for y, value in enumerate(row):
            if value == 'S':
                start = Point(x, y)
            if value == 'E':
                end = Point(x, y)
    assert start
    assert end

    return start, end


def paint_path(grid: Grid, path: List[Point]):
    temp_grid = copy.deepcopy(grid)
    for point in path:
        temp_grid.set_value(point, "X")
    print(temp_grid)

def find_best_path(start: Point, end: Point, grid: Grid, start_direction: Direction):
    pq = [(0, start, [start], start_direction)]
    visited = set()
    min_points = float('inf')
    best_paths = []
    while pq:
        points, current_point, path, current_dir = heapq.heappop(pq)
        if points > min_points:
            continue
        path.append(current_point)
        visited.add(f"{current_point.x}-{current_point.y}-{current_dir.symbol}")
        if current_point == end:
            if points <= min_points:
                min_points = points
                best_paths.append(path)
            continue

        for direction in directions:
            # ignore backing up direction
            if direction.change_x * -1 == current_dir.change_x and direction.change_y * -1 == current_dir.change_y:
                continue

            next_point = direction.next_point(current_point)

            if not grid.in_bounds(next_point) or grid.get_value(next_point) == '#' or f"{next_point.x}-{next_point.y}-{direction.symbol}" in visited:
                continue

            step = 1
            direction_change_point = 1000 if direction != current_dir else 0
            new_points = points + step + direction_change_point
            heapq.heappush(pq, (new_points, next_point, path + [next_point], direction))

    return best_paths, min_points

grid = get_data('day16.input')
start, end = get_start_end(grid)



paths, points = find_best_path(start, end, grid, start_direction)
tiles = set()
for path in paths:
    for point in path:
        tiles.add(point)


print("Part A:", points)
print("Part B:", len(tiles))