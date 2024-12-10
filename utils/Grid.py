from utils.Point import Point


class Grid:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.grid = []

    def in_bounds(self, point: Point):
        return 0 <= point.x < self.length and 0 <= point.y < self.width

    @staticmethod
    def from_str(content: str):
        grid = []
        for line in content.split("\n"):
            grid.append([x for x in line.strip()])
        width = len(grid[0])
        heigth = len(grid)
        new_grid = Grid(width, heigth)
        new_grid.grid = grid
        return new_grid


    def get_value(self, point: Point):
        if self.in_bounds(point):
            return self.grid[point.x][point.y]

    def set_value(self, point: Point, value: str):
        self.grid[point.x][point.y] = value

    def __str__(self):
        text =  f"Width: {self.width}\t Heigth: {self.length}"
        for line in self.grid:
            text += f"\n{' '.join(line)}"
        return text
