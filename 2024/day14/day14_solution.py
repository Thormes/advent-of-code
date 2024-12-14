import copy
import re

from PIL import Image

from typing import List, Tuple

from utils.Grid import Grid
from utils.Point import Point


class Robot:
    def __init__(self, starting_position: Point, change_x: int, change_y: int):
        self.starting_position = starting_position
        self.current_position = starting_position
        self.change_x = change_x
        self.change_y = change_y

    def move(self, height, width):
        start = self.current_position
        next_x = (start.x + self.change_x) % height
        next_y = (start.y + self.change_y) % width
        self.current_position = Point(next_x, next_y)

    def get_coords(self):
        return (self.current_position.x, self.current_position.y)

    def __str__(self):
        return f'Starting:{self.starting_position}\tCurrent:{self.current_position}'


def get_robots(filename: str) -> List[Robot]:
    with open(filename) as text_input:
        lines = text_input.readlines()

    robots = []
    for line in lines:
        pattern = r'p=(\d+),(\d+) v=(.*),(.*)'
        numbers = re.search(pattern, line)
        [px, py, rx, ry] = numbers.groups()
        robot = Robot(Point(int(py), int(px)), int(ry), int(rx))
        robots.append(robot)

    return robots


def move_robots(robots: List[Robot], grid):
    for robot in robots:
        robot.move(grid.length, grid.width)


def get_quadrants(grid: Grid) -> Tuple[List[List[str]], List[List[str]], List[List[str]], List[List[str]]]:
    mid_x = grid.length // 2
    mid_y = grid.width // 2
    q1 = grid.slice(0, 0, mid_x, mid_y)
    q2 = grid.slice(0, mid_y + 1, mid_x, grid.width)
    q3 = grid.slice(mid_x + 1, 0, grid.length, mid_y)
    q4 = grid.slice(mid_x + 1, mid_y + 1, grid.length, grid.width)

    return (q1, q2, q3, q4)


def total_robots(quadrant: List[List[str]]):
    total = 0
    for row in quadrant:
        for value in row:
            if value.isdigit():
                total += int(value)
    return total


def place_robots(grid: Grid, robots: List[Robot]) -> Grid:
    local_grid = copy.deepcopy(grid)
    for robot in robots:
        if not local_grid.grid[robot.current_position.x][robot.current_position.y].isdigit():
            local_grid.grid[robot.current_position.x][robot.current_position.y] = "0"

        local_grid.grid[robot.current_position.x][robot.current_position.y] = str(
            int(local_grid.grid[robot.current_position.x][robot.current_position.y]) + 1)
    return local_grid


def create_image(grid: Grid, iteration: int):
    height, width = grid.length, grid.width
    image = Image.new("1", (width, height))
    for x in range(grid.width):
        for y in range(grid.length):
            value = grid.grid[y][x]
            if value.isdigit():
                try:
                    image.putpixel((x, y), 1)
                except:
                    print(x, y)
    image.save(f'./iterations/{iteration}.png')


def get_part_A():
    robots = get_robots('day14.input')
    grid = Grid(101, 103)
    grid.fill('.')
    for i in range(100):
        move_robots(robots, grid)

    grid = place_robots(grid, robots)
    return grid


def get_part_B():
    robots = get_robots('day14.input')
    grid = Grid(101, 103)
    grid.fill('')
    local = copy.copy(grid)
    for i in range(10):
        move_robots(robots, grid)
        local = place_robots(grid, robots)
        create_image(local, i + 1)




full = get_part_A()
quadrandts = get_quadrants(full)
safety = 1
for quadrant in quadrandts:
    safety *= total_robots(quadrant)

print(safety)

get_part_B()
