class Point:
    def __init__(self, x: int = None, y: int = None):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __hash__(self):
        return f"({self.x},{self.y})"

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)