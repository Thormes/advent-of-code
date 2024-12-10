import copy
from typing import Tuple, Optional, List, Set

from utils import Point, Grid


class ValuePoint:
    def __init__(self, value: int, point: Point.Point):
        self.value = value
        self.point = point
        self.valid_adjacents: list[ValuePoint] = []

    def get_coord(self) -> Tuple[int, int]:
        return self.point.x, self.point.y

    def increase_adjacent(self, next_point: 'ValuePoint'):
        # Not adjacent
        if abs(self.point.x - next_point.point.x) != 1 and abs(self.point.y - next_point.point.y) != 1:
            return False

        # Not increasing value
        if self.value + 1 != next_point.value:
            return False

        return True

    def __repr__(self):
        return f"({self.point.x},{self.point.y}) - {self.value}"

    def __eq__(self, other):
        return other.point.x == self.point.x and other.point.y == self.point.y

    def __hash__(self):
        return hash((self.point.x, self.point.y))

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_grid_from_data(filename: str) -> Grid.Grid:
    with open(filename) as file:
        grid = Grid.Grid.from_str(file.read())

    return grid


def get_points(grid: Grid.Grid) -> dict[str, ValuePoint]:
    values = {}
    for i in range(grid.length):
        for j in range(grid.width):
            point = Point.Point(i, j)
            value_point = ValuePoint(int(grid.grid[i][j]), point)
            values[f"{value_point.point.x}-{value_point.point.y}"] = value_point

    return values


def dfs_a(visited: set[Tuple[int, int]], node: ValuePoint):
    if node.get_coord() not in visited:
        if node.value == 9:
            visited.add(node.get_coord())
        for adjacent in node.valid_adjacents:
            dfs_a(visited, adjacent)


def find_all_paths(root: ValuePoint) -> List[List[ValuePoint]]:
    def dfs_b(current: ValuePoint, path: List[ValuePoint], visited: Set[ValuePoint])->List[List[ValuePoint]]:
        if current.value == 9:
            return [path]

        all_paths = []

        for adjacent in current.valid_adjacents:
            if adjacent not in visited:
                new_path = path + [adjacent]
                new_visited = visited.copy()
                new_visited.add(adjacent)

                sub_paths = dfs_b(adjacent, new_path, new_visited)
                all_paths.extend(sub_paths)

        return all_paths

    initial_path = [root]
    initial_visited = {root}
    return dfs_b(root, initial_path, initial_visited)

def build_graph(points: dict[str, ValuePoint]):
    for coord, point in points.items():
        for direction in directions:
            next_point = points.get(f"{point.point.x + direction[0]}-{point.point.y + direction[1]}", None)
            if not next_point: continue
            if point.increase_adjacent(next_point):
                point.valid_adjacents.append(next_point)


def get_trailvalues(points: dict[str, ValuePoint], value: int):
    trailpoints = []
    for repr, point in points.items():
        if point.value == value:
            trailpoints.append(point)

    return trailpoints


data_grid = get_grid_from_data("day10.input")
points = get_points(data_grid)
build_graph(points)
heads = get_trailvalues(points, 0)
total_a = 0
total_b = 0
for head in heads:
    visited = set()
    dfs_a(visited, head)
    total_a += len(visited)
    paths = find_all_paths(head)
    total_b += len(paths)

print("Part A:",total_a)
print("Part B:", total_b)
