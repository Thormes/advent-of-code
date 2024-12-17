from typing import Optional

from utils.Point import Point


class Direction:
    def __init__(self, name: str, change_x: int, change_y: int):
        self.name = name
        self.symbol = ""
        self.change_x = change_x
        self.change_y = change_y
        self.next_direction: Optional[Direction] = None
        self.previous_direction: Optional[Direction] = None
        if self.change_x == 0:
            self.main_axis = 'x'
            self.secondary_axis = 'y'
        else:
            self.main_axis = 'y'
            self.secondary_axis = 'x'
        match self.name:
            case "up":
                self.symbol = "^"
            case "down":
                self.symbol = "v"
            case "right":
                self.symbol = ">"
            case "left":
                self.symbol = "<"

    def __str__(self):
        return self.name

    def next_point(self, point: Point):
        return Point(point.x + self.change_x, point.y + self.change_y)

    def previous_point(self, point: Point):
        return Point(point.x - self.change_x, point.y - self.change_y)

    def curve_point(self, origin: Point, obstacle: Point) -> Point:
        curve_point = Point()
        curve_point[self.main_axis] = origin[self.main_axis]
        curve_point[self.previous_direction.main_axis] = obstacle[self.previous_direction.main_axis]
        return curve_point

    def reachable(self, origin: Point, destination: Point, existing_obstacle) -> bool:
        #not the same direction, not reachable
        if destination[self.main_axis] != origin[self.main_axis]:
            return False

        diff = abs(destination[self.secondary_axis] - origin[self.secondary_axis])
        ## it's the same point
        if diff == 0:
            return False

        new_diff = 99999999
        while new_diff > 0:
            origin = self.next_point(origin)
            new_diff = abs(destination[self.secondary_axis] - origin[self.secondary_axis])

            ## if the diff is increasing, it's walking in opposite direction
            if new_diff > diff:
                return False

            ## if hit obstacle, is not reachable
            if origin == existing_obstacle:
                return False

        return True
