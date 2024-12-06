import copy
from typing import Optional, List, Dict


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __repr__(self):
        return f"({self.x},{self.y})"
    def __hash__(self):
        return f"({self.x},{self.y})"


class Direction:
    def __init__(self, name: str, change_x: int, change_y: int):
        self.name = name
        self.change_x = change_x
        self.change_y = change_y
        self.next_direction: Optional[Direction] = None

    def next_point(self, point: Point):
        if self.change_x != 0:
            return Point(point.x + self.change_x, point.y)

        return Point(point.x, point.y + self.change_y)


class InloopException(Exception):
    def __init__(self):
        self.message = "Em loop"


path = []
directions = [
    Direction('up', -1, 0),
    Direction('right', 0, 1),
    Direction('down', 1, 0),
    Direction('left', 0, -1)
]
for i in range(len(directions)):
    directions[i].next_direction = directions[(i + 1) % len(directions)]


def get_direction_by_name(name: str) -> Direction:
    for direction in directions:
        if direction.name == name:
            return direction

    raise ValueError("Direction not Found")


with open("day6.input") as text_input:
    count = 0
    for line in text_input.readlines():
        path.append([x for x in line.strip()])
        if "^" in line:
            initial = Point(count, line.index("^"))
            path[initial.x][initial.y] = "X"

        count += 1


def traverse(lab: list[list[str]], position: Point, direction: Direction) -> tuple[
    int, Dict[str, List[Point]], Dict[str, List[Point]]]:
    found_obstacles = {direction.name: []}
    points_travelled = {direction.name: []}
    steps = 1
    width = len(lab[0])
    height = len(lab)
    while height > position.y >= 0 and width > position.x >= 0:
        next_position = direction.next_point(position)
        if next_position in found_obstacles[direction.name]:
            raise InloopException
        # out of bounds
        if next_position.y == height or next_position.x == width:
            break
        value = lab[next_position.x][next_position.y]
        if value == '.':
            steps += 1
            lab[next_position.x][next_position.y] = 'X'
            points_travelled[direction.name].append(next_position)
        elif value == '#':
            found_obstacles[direction.name].append(next_position)
            direction = direction.next_direction
            if not found_obstacles.get(direction.name, None):
                found_obstacles[direction.name] = []
            if not points_travelled.get(direction.name, None):
                points_travelled[direction.name] = []
            continue
        position = next_position
    return steps, found_obstacles, points_travelled


start_direction = directions[0]
start_position = initial
original_lab = copy.deepcopy(path)

total, obstacles, travelled = traverse(path, start_position, start_direction)
print(total)

count = 0
for direction, positions in travelled.items():
    direct = get_direction_by_name(direction)
    for point in positions:
        lab = copy.deepcopy(original_lab)
        lab[point.x][point.y] = '#'
        try:
            traverse(lab, start_position, start_direction)
        except InloopException:
            count += 1


print(count)