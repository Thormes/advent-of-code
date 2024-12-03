import re
from typing import Iterator

pattern = r'mul\(\d{1,3},\d{1,3}\)'
pattern_numbers = r'\d{1,3}'

with open("day3.input") as entry:
    input_text = entry.read()


def get_mulinstructions(input: str) -> Iterator[str]:
    acumulator = ''
    disabled = False
    for s in input:
        acumulator += s
        if 'do()' in acumulator:
            acumulator = ''
            disabled = False
        if "don't()" in acumulator:
            acumulator = ''
            disabled = True
        found = re.search(pattern, acumulator)
        if found and not disabled:
            yield found.group(0)
            acumulator = ''


total = 0
for instruction in get_mulinstructions(input_text):
    numbers = [int(x) for x in re.findall(pattern_numbers, instruction)]
    if len(numbers) != 2:
        raise ValueError("Instruction have more than 2 numbers")
    total += (numbers[0] * numbers[1])

print(total)
