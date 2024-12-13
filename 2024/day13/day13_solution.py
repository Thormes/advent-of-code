import re
from utils.Point import Point
import numpy as np


class Button:
    def __init__(self, X: int, Y: int):
        self.X = X
        self.Y = Y


class Machine:
    def __init__(self, A: Button, B: Button, prize: Point):
        self.A = A
        self.B = B
        self.prize = prize
        self.tokensA = 0
        self.tokensB = 0
        self.price = None

    def get_tokens(self):
        # A*Y + B*Y = Prize.Y
        # A*X + B*X = Prize.x

        A = np.array([[self.A.X, self.B.X], [self.A.Y, self.B.Y]])
        B = np.array([self.prize.x, self.prize.y])

        try:
            solution = np.linalg.solve(A, B)
            X, Y = solution
            print(X, Y)
            # has integer solution
            if round(X) == round(X,3) and round(Y) == round(Y,3):
                self.tokensA = round(X)
                self.tokensB = round(Y)
                self.price = self.tokensA * 3 + self.tokensB

        except np.linalg.LinAlgError:
            pass



def get_cases(filename, part_b: bool):
    with open(filename) as text_input:
        cases = text_input.read().split("\n\n")

    pattern_button = r'X\+(\d+), Y\+(\d+)'
    pattern_prize = r'X=(\d+), Y=(\d+)'
    machines = []
    base = 0
    if part_b:
        base = 10000000000000

    for case in cases:
        lines = case.split("\n")
        A = re.search(pattern_button, lines[0])
        B = re.search(pattern_button, lines[1])
        Prize = re.search(pattern_prize, lines[2])
        buttonA = Button(int(A.group(1)), int(A.group(2)))
        buttonB = Button(int(B.group(1)), int(B.group(2)))
        prize = Point(int(Prize.group(1)) + base, int(Prize.group(2)) + base)
        machine = Machine(buttonA, buttonB, prize)
        machines.append(machine)
    return machines


machines = get_cases('day13.input', True)
total = 0
for machine in machines:
    machine.get_tokens()
    if not machine.price:
        print("\tUnsolvable")
    else:
        print(machine.price)
        total += machine.price
        #total += machine.tokensB + (machine.tokensA * 3)

print(total)
