import copy
import math
import re


class Computer:
    def __init__(self):
        self.registerA = 0
        self.registerB = 0
        self.registerC = 0
        self.pointer = 0
        self.program = []
        self.output = []
        self.opcodes = {"0": self.adv,
                        "1": self.bxl,
                        "2": self.bst,
                        "3": self.jnz,
                        "4": self.bxc,
                        "5": self.out,
                        "6": self.bdv,
                        "7": self.cdv
                        }

    def reset(self):
        self.pointer = 0
        self.output = []
        self.registerC = 0
        self.registerB = 0
        self.registerA = 0

    def execute_instruction(self, opcode: str, operand: str):
        func = self.opcodes[opcode]
        func(operand)

    def print_output(self):
        return (",".join(str(v) for v in self.output))

    def parseOperand(self, operand: str) -> int:
        match operand:
            case "0" | "1" | "2" | "3" | "7":
                return int(operand)
            case "4":
                return self.registerA
            case "5":
                return self.registerB
            case "6":
                return self.registerC

    def adv(self, operand: str):
        numerator = self.registerA
        value = self.parseOperand(operand)
        #print(f"2 to the power of {value}")
        denominator = 2 ** value
        #print(f"divide {numerator} by {denominator}")
        self.registerA = numerator // denominator

    def bdv(self, operand: str):
        numerator = self.registerA
        value = self.parseOperand(operand)
        #print(f"2 to the power of {value}")
        denominator = 2 ** value
        #print(f"divide {numerator} by {denominator}")
        self.registerB = numerator // denominator

    def cdv(self, operand: str):
        numerator = self.registerA
        value = self.parseOperand(operand)
        #print(f"2 to the power of {value}")
        denominator = 2 ** value
        self.registerC = numerator // denominator
        #print(f"divide {numerator} by {denominator}")

    def bxl(self, operand: str):
        literal = int(operand)
        on_register = self.registerB
        #print(f"Result of {on_register} ^ {literal}: {on_register ^ literal}")
        self.registerB = on_register ^ literal

    def bst(self, operand: str):
        value = self.parseOperand(operand)
        #print(f"RegisterB receives {value} % 8: {value % 8}")
        self.registerB = value % 8

    def jnz(self, operand: str):
        if self.registerA == 0:
            return
        #print(f"Jump to {operand}")
        self.pointer = int(operand) - 2

    def bxc(self, operand: str):
        #print(f"Register B receives {self.registerB} ^ {self.registerC}: {self.registerB ^ self.registerC}")
        self.registerB = self.registerB ^ self.registerC

    def out(self, operand: str):
        value = self.parseOperand(operand)
        #print(f"Put {value} % 8 ({value % 8}) in output")
        self.output.append(value % 8)

    def run(self):
        while self.pointer < len(self.program):
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            self.execute_instruction(opcode, operand)
            self.pointer += 2


def create_pc(filename: str):
    pc = Computer()
    with open(filename) as text_input:
        register_input, program_input = text_input.read().split("\n\n")
        program = program_input.split(":")[1].strip().split(",")
        register_lines = register_input.split("\n")
        pc.registerA = int(re.sub(r"\D", "", register_lines[0]))
        pc.registerB = int(re.sub(r"\D", "", register_lines[1]))
        pc.registerC = int(re.sub(r"\D", "", register_lines[2]))
        pc.program = program

    return pc


def solve_a():
    pc = create_pc('day17.input')
    pc.run()
    print(pc.print_output())


def solve_b():
    pc = create_pc('day17.input')
    candidates = [0]
    for l in range(len(pc.program)):
        next_candidates = []
        for val in candidates:
            for i in range(8):
                target = (val << 3) + i
                pc.registerA = target
                pc.run()
                response = list(map(str, pc.output))
                if response == pc.program[-l -1:]:
                    next_candidates.append(target)
                pc.reset()
        candidates = next_candidates
        print(candidates)

    return min(candidates)


print(solve_b())
