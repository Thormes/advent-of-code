import copy
from typing import Dict, List

from utils.Grid import Grid
from utils.Point import Point


def get_antinodes_A(antennas: dict[str, list[Point]], grid: Grid):
    antinodes = []
    for antenna, positions in antennas.items():
        ammount = len(positions)
        for i in range(ammount):
            for j in range(i + 1, ammount):
                primeiro = positions[i]
                segundo = positions[j]
                antinode1 = Point(primeiro.x - (segundo.x - primeiro.x), primeiro.y - (segundo.y - primeiro.y))
                antinode2 = Point(segundo.x + (segundo.x - primeiro.x), segundo.y + (segundo.y - primeiro.y))
                if grid.in_bounds(antinode1) and antinode1 not in antinodes:
                    antinodes.append(antinode1)
                if grid.in_bounds(antinode2) and antinode2 not in antinodes:
                    antinodes.append(antinode2)
    return antinodes

def get_antinodes_B(antennas: dict[str, list[Point]], grid: Grid):
    antinodes = []
    for antenna, positions in antennas.items():
        ammount = len(positions)
        if ammount == 1:
            continue
        for i in range(ammount):
            for j in range(i + 1, ammount):
                first = positions[i]
                second = positions[j]

                #side 1
                point_1 = copy.deepcopy(first)
                while grid.in_bounds(point_1):
                    if grid.in_bounds(point_1) and point_1 not in antinodes:
                        grid.set_value(point_1, '#')
                        antinodes.append(point_1)
                    point_1 = Point(point_1.x - (second.x - first.x), point_1.y - (second.y - first.y))

                #side 2
                point_2 = copy.deepcopy(second)
                while grid.in_bounds(point_2):
                    if grid.in_bounds(point_2) and point_2 not in antinodes:
                        antinodes.append(point_2)
                        grid.set_value(point_2, '#')
                    point_2 = Point(point_2.x + (second.x - first.x), point_2.y + (second.y - first.y))
    return antinodes


def get_data(file: str) -> tuple[Grid, Dict[str, List[Point]]]:
    antennas: dict[str, list[Point]] = {}

    with open(file) as text_input:
        count = 0
        for line in text_input.readlines():
            length = len(line.strip())
            for j in range(len(line.strip())):
                # Is antenna
                if line[j] != '.':
                    antenna = line[j]
                    if not antennas.get(antenna, None):
                        antennas[antenna] = []
                    antennas[antenna].append(Point(count, j))
            count += 1
        text_input.seek(0)
        grid = Grid.from_str(text_input.read())
    return grid, antennas


grid, antennas = get_data("day8.input")
antinodesA = get_antinodes_A(antennas, grid)
antinodesB = get_antinodes_B(antennas, grid)
print(len(antinodesA))
print(len(antinodesB))
