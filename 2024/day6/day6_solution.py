import copy
from typing import Optional, List, Dict
from utils.Point import Point
from utils.Direction import Direction

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
    directions[i].previous_direction = directions[i - 1] if i > 0 else directions[len(directions) - 1]


def get_direction_by_name(name: str) -> Direction:
    for direction in directions:
        if direction.name == name:
            return direction

    raise ValueError("Direction not Found")


with open("day6.test") as text_input:
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

#
# for direction, obstacle_list in obstacles.items():
#     curr_direction = get_direction_by_name(direction)
#     previous_direction = curr_direction.previous_direction
#     for obstacle in obstacle_list:
#
#         print(direction, obstacle)
#         for prev_obstacle in obstacles[previous_direction.name]:
#             #If it hits in different directions, skip
#             if obstacle == prev_obstacle:
#                 continue
#
#             curve_point = curr_direction.curve_point(obstacle, prev_obstacle)
#             would_hit = False
#             for recursive_obstacle in obstacles[previous_direction.name]:
#                 reachable = previous_direction.reachable(curve_point, prev_obstacle, recursive_obstacle)
#                 if reachable:
#                     would_hit = True
#                     break
#             if would_hit:
#                 print("Would Hit:")
#                 print("Curve:", curve_point, "\tPrevious Obstacle:", prev_obstacle)
#                 print("Obstacle Position:", previous_direction.next_point(curve_point))
#             else:
#                 print("Could not Hit\n", "Curve:", curve_point, "\tPrevious Obstable:",prev_obstacle)
#         print()
print(count)
