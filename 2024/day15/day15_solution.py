from typing import Tuple, List, Optional
from collections import deque

from utils.Direction import Direction
from utils.Grid import Grid
from utils.Point import Point

directions_map = {
    "^": Direction('up', -1, 0),
    ">": Direction('right', 0, 1),
    "v": Direction('down', 1, 0),
    "<": Direction('left', 0, -1)
}


class Box:
    def __init__(self, left: Point, right: Point):
        self.left = left
        self.right = right
        self.movable_boxes: List['Box'] = []

    def __eq__(self, other: 'Box'):
        return self.left == other.left and self.right == other.right

    @staticmethod
    def get_by_left_point(left_point: Point, boxes: List['Box']) -> Optional['Box']:
        for box in boxes:
            if left_point == box.left:
                return box
        return None

    @staticmethod
    def get_by_right_point(right_point: Point, boxes: List['Box']) -> Optional['Box']:
        for box in boxes:
            if right_point == box.right:
                return box
        return None

    def can_be_moved(self, direction: Direction, grid: Grid, boxes: List['Box']):
        next_point_left = direction.next_point(self.left)
        self.movable_boxes = []
        if direction.name == 'right' or direction.name == 'left':
            while grid.get_value(next_point_left) != '.':

                next_box = Box.get_by_left_point(next_point_left, boxes)
                if next_box and next_box not in self.movable_boxes:
                    self.movable_boxes.append(next_box)
                if grid.get_value(next_point_left) == '#':
                    self.movable_boxes = []
                    return False
                next_point_left = direction.next_point(next_point_left)
            self.movable_boxes.reverse()
            return True
        else:
            next_point_right = direction.next_point(self.right)
            #touching another box, can only be moved if the next box can be moved
            can_move_left = False
            can_move_right = False
            if grid.get_value(next_point_left) == '[':
                box = self.get_by_left_point(next_point_left, boxes)
                can_move_left = box.can_be_moved(direction, grid, boxes)
                if can_move_left and box not in self.movable_boxes:
                    self.movable_boxes.append(box)
            elif grid.get_value(next_point_left) == ']':
                box = self.get_by_right_point(next_point_left, boxes)
                can_move_left = box.can_be_moved(direction, grid, boxes)
                if can_move_left and box not in self.movable_boxes:
                    self.movable_boxes.append(box)
            elif grid.get_value(next_point_left) == '.':
                can_move_left = True

            if grid.get_value(next_point_right) == ']':
                box = self.get_by_right_point(next_point_right, boxes)
                can_move_right = box.can_be_moved(direction, grid, boxes)
                if can_move_right and box not in self.movable_boxes:
                    self.movable_boxes.append(box)
            elif grid.get_value(next_point_right) == '[':
                box = self.get_by_left_point(next_point_right, boxes)
                can_move_right = box.can_be_moved(direction, grid, boxes)
                if can_move_right and box not in self.movable_boxes:
                    self.movable_boxes.append(box)
            elif grid.get_value(next_point_right) == '.':
                can_move_right = True

            return can_move_right and can_move_left

    def move_box(self, direction: Direction, grid: Grid):
        for movable in self.movable_boxes:
            movable.move_box(direction, grid)
        self.movable_boxes = []

        grid.grid[self.left.x][self.left.y] = '.'
        grid.grid[self.right.x][self.right.y] = '.'
        self.left = direction.next_point(self.left)
        self.right = direction.next_point(self.right)
        grid.grid[self.left.x][self.left.y] = '['
        grid.grid[self.right.x][self.right.y] = ']'

    def clear_movable(self):
        for movable in self.movable_boxes:
            movable.clear_movable()
        self.movable_boxes = []


def get_data(filename) -> Tuple[Grid, List[Direction]]:
    with open(filename) as text_input:
        data = text_input.read()

    grid_part, movements = data.split("\n\n")
    grid = Grid.from_str(grid_part)
    robot_directions = []
    for movement_line in movements.split("\n"):
        for movement in movement_line:
            robot_directions.append(directions_map[movement])

    return grid, robot_directions


def process_movements_a(filename) -> Grid:
    def can_move_boxes(start_point: Point, direction: Direction, grid: Grid):
        next_point = direction.next_point(start_point)
        while grid.get_value(next_point) != '.':
            if grid.get_value(next_point) == '#':
                return False
            next_point = direction.next_point(next_point)

        return True

    grid, movements = get_data(filename)
    for i in range(grid.length):
        for j in range(grid.width):
            if grid.grid[i][j] == '@':
                robot_start = Point(i, j)

    curr_point_robot = robot_start

    for movement in movements:
        box_moves = deque()
        next_point_robot = movement.next_point(curr_point_robot)
        next_value = grid.get_value(next_point_robot)
        #does not move
        if next_value == '#':
            continue

        # check if hit box(es) and can move them, if not, next movement
        next_point = next_point_robot
        if next_value == 'O' and not can_move_boxes(next_point, movement, grid):
            continue

        #move boxes
        while next_value == 'O':
            box_moves.append(next_point)
            next_point = movement.next_point(next_point)
            next_value = grid.get_value(next_point)

        while len(box_moves) > 0:
            box_point = box_moves.pop()
            next_box_point = movement.next_point(box_point)
            grid.set_value(next_box_point, 'O')
            grid.set_value(box_point, '.')

        # take step
        grid.set_value(curr_point_robot, '.')
        curr_point_robot = movement.next_point(curr_point_robot)
        grid.set_value(curr_point_robot, '@')

    return grid


def create_boxes(grid: Grid) -> List[Box]:
    boxes = []
    for x in range(grid.length):
        for y in range(0, grid.width, 2):
            if grid.grid[x][y] == '[':
                box = Box(Point(x, y), Point(x, y + 1))
                boxes.append(box)

            if grid.grid[x][y] == ']':
                box = Box(Point(x, y - 1), Point(x, y))
                boxes.append(box)

    return boxes


def process_movements_b(filename) -> Tuple[Grid, List[Box]]:
    txt = ''
    grid, movements = get_data(filename)
    widen_grid(grid)
    boxes = create_boxes(grid)
    #txt = 'Original\n' + str(grid) + "\n"
    print(grid)
    box_count = 1
    for i in range(grid.length):
        for j in range(grid.width):
            if grid.grid[i][j] == '@':
                robot_start = Point(i, j)

    curr_point_robot = robot_start
    count = 0
    for movement in movements:
        count += 1
        #txt += f'\n{count} - {str(movement)}\n'
        next_point_robot = movement.next_point(curr_point_robot)
        next_value = grid.get_value(next_point_robot)
        #does not move
        if next_value == '#':
            txt += str(grid) + "\n"
            continue

        # check if hit box(es) and can move them, if not, next movement
        next_point = next_point_robot
        if next_value == '[':
            box = Box.get_by_left_point(next_point, boxes)
            if box.can_be_moved(movement, grid, boxes):
                box.move_box(movement, grid)
            else:
                box.clear_movable()
                txt += str(grid) + "\n"
                continue

        if next_value == ']':
            box = Box.get_by_right_point(next_point, boxes)
            if box.can_be_moved(movement, grid, boxes):
                box.move_box(movement, grid)
            else:
                box.clear_movable()
                txt += str(grid) + "\n"
                continue

        # take step
        grid.set_value(curr_point_robot, '.')
        curr_point_robot = movement.next_point(curr_point_robot)
        grid.set_value(curr_point_robot, '@')
        txt += str(grid) + "\n"

    with open('processamento.txt', 'w', encoding='utf-8') as file:
        file.write(txt)

    return grid, boxes


def calculate_coordinates_a(grid: Grid) -> int:
    total = 0
    for x in range(grid.length):
        for y in range(grid.width):
            if grid.grid[x][y] == 'O':
                value = 100 * x + y
                total += value

    return total


def calculate_coordinates_b(grid: Grid, boxes: List[Box]) -> int:
    total = 0
    for y, row in enumerate(map):
        for x, block in enumerate(row):
            if block in "O[":
                total += y * 100 + x
    return total


def widen_grid(grid: Grid):
    for x in range(grid.length):
        i = 0
        while i < len(grid.grid[x]):
            curr_value = grid.grid[x][i]
            if curr_value == '.' or curr_value == '@':
                grid.grid[x].insert(i + 1, '.')
            if curr_value == '#':
                grid.grid[x].insert(i + 1, '#')

            if curr_value == 'O':
                grid.grid[x][i] = '['
                grid.grid[x].insert(i + 1, ']')

            i += 2
    grid.width *= 2


# grid_a = process_movements_a('day15.input')
#
# print(grid_a)
# print(calculate_coordinates_a(grid_a))

grid_b, movements = get_data('day15.test')
print(grid_b)
processed_grid, final_boxes = process_movements_b('day15.input')
print(processed_grid)
print(calculate_coordinates_b(processed_grid, final_boxes))

