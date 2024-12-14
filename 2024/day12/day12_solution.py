# formula points * 4 - (2 * neighbours)
import random
from typing import List, Dict, Optional

from utils.Grid import Grid
from utils.Point import Point

# up, right, down, left
directions = [(-1, -0), (0, 1), (1, 0), (0, -1)]


def generate_color():
    r = random.randint(27, 230)
    g = random.randint(27, 230)
    b = random.randint(27, 230)
    return f'#{r:x}{g:x}{b:x}'


class Plot:
    def __init__(self, value: str, point: Point):
        self.value = value
        self.point = point
        self.neighbours = []

    def calculate_neighbours(self, all_plots: Dict[str, List['Plot']], grid: Grid):
        for direction in directions:
            next_point = Point(self.point.x + direction[0], self.point.y + direction[1])
            if not grid.in_bounds(next_point):
                continue
            for plot in all_plots[self.value]:
                if plot.point == next_point:
                    self.neighbours.append(plot)

    def get_coord(self):
        return self.point.x, self.point.y

    def __str__(self):
        return f"{self.value} - ({self.point.x},{self.point.y})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.point)


class Region:
    def __init__(self, seed: str):
        self.seed = seed
        self.plots = []
        self.area = 0
        self.outer_perimeter = 0
        self.inner_perimeter = 0
        self.upper_left = None
        self.upper_right = None
        self.lower_left = None
        self.lower_right = None
        self.inner_regions: List['Region'] = []
        self.outer_region: Optional['Region'] = None
        self.color = generate_color()

    def in_region(self, seed: str, point: Point):
        if seed != self.seed:
            return False
        for plot in self.plots:
            if plot.point == point:
                return True
        return False

    def __str__(self):
        txt = f"Seed:{self.seed}\t\tOuter:{self.outer_perimeter}\t\tInner:{self.inner_perimeter}\t\tArea:{self.area}\t\tPrice:{self.area * self.outer_perimeter}\t\tStart:{self.upper_left}\n"
        for reg in self.inner_regions:
            txt += "\tInner Region: " + str(reg)
        return txt

    def fill_region(self, start_plot: Plot):
        if start_plot not in self.plots:
            self.plots.append(start_plot)
            for neighbour in start_plot.neighbours:
                self.fill_region(neighbour)

    def is_inside(self, other_region: 'Region', grid: Grid):
        for plot in self.plots:
            for direction in directions:
                neighbour = Point(plot.point.x + direction[0], plot.point.y + direction[1])
                if not grid.in_bounds(neighbour):
                    return False
                if not self.in_region(self.seed, neighbour) and not other_region.in_region(grid.grid[neighbour.x][neighbour.y], neighbour):
                    return False
        return True

    def correct_perimeter(self):
        for region in self.inner_regions:
            self.inner_perimeter += region.outer_perimeter

    def calculate_region(self):
        self.area = len(self.plots)
        perimeter = 4 * self.area
        self.lower_right = self.plots[0]
        self.upper_right = self.plots[0]
        self.lower_left = self.plots[0]
        self.upper_left = self.plots[0]
        for plot in self.plots:
            perimeter -= len(plot.neighbours)
            if plot.point.x <= self.upper_left.point.x and plot.point.y <= self.upper_left.point.y:
                self.upper_left = plot
            if plot.point.x <= self.upper_right.point.x and plot.point.y >= self.upper_right.point.y:
                self.upper_right = plot
            if plot.point.x >= self.lower_left.point.x and plot.point.y <= self.lower_left.point.y:
                self.lower_left = plot
            if plot.point.x >= self.lower_right.point.x and plot.point.y >= self.lower_right.point.y:
                self.lower_right = plot
        self.outer_perimeter = perimeter
        self.inner_perimeter = perimeter


def get_data(filename: str) -> Grid:
    with open(filename) as input_data:
        grid = Grid.from_str(input_data.read())

    return grid


def create_html(grid: Grid, regions: List[Region]):
    txt = '''<html>
            <head>
            <style>
                .row {
                display: flex;
                justify-content: space-between;
                }
                .row td{
                width: 20px;
                heigth: 20px;
                text-align: center;
                padding: 10px;
                }
                .row .number{
                font-weight: bold;
                width: 20px;
                }
                .coord{
                font-size: 0.5em;
                }
            </style>
            </head>
            <body>
            <table>
            <tbody>
            '''
    for row in range(grid.length):
        txt += '\n<tr class="row">'
        for col in range(grid.width):
            point = Point(row, col)
            for region in regions:
                if region.in_region(grid.grid[row][col], point):
                    if region.outer_region:
                        change_color = ";color:white;"
                    else:
                        change_color = ''
                    txt += f'<td id="{row}-{col}" style="background-color: {region.color}{change_color}">{grid.grid[row][col]}<div class="coord">{row},{col}</div></td>'
                    break
        txt += '</tr>'
    txt += '\n</tbody></table>\n</body>\n</html>'
    return txt


grid = get_data('day12.input')
all_plots = {}

for row in range(grid.length):
    for col in range(grid.width):
        seed = grid.grid[row][col]
        if not all_plots.get(seed, None):
            all_plots[seed] = []

        individual_plot = Plot(grid.grid[row][col], Point(row, col))
        all_plots[seed].append(individual_plot)

regions = []
counted = []
for seed, plots in all_plots.items():
    for plot in plots:
        plot.calculate_neighbours(all_plots, grid)
    for plot in plots:
        if plot not in counted:
            region = Region(seed)
            region.fill_region(plot)
            region.calculate_region()
            regions.append(region)
            counted.extend(region.plots)

for i in range(len(regions)):
    for j in range(len(regions)):
        if i == j:
            continue
        if regions[i].is_inside(regions[j], grid):
            regions[j].inner_regions.append(regions[i])
            regions[i].outer_region = regions[j]

for region in regions:
    region.correct_perimeter()

html = create_html(grid, regions)

with open('grid.html', 'w', encoding='utf-8') as html_grid:
    html_grid.write(html)

total_a = 0
for region in regions:
    total_a += region.area * region.outer_perimeter
print("Part A:",total_a)
