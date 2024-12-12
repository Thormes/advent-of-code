from typing import List, Dict


def get_inital_data(filename) -> Dict[str, int]:
    with open(filename) as data_input:
        stones = data_input.read().strip().split(" ")

    stone_map = {}
    for stone in stones:
        if not stone_map.get(stone, None):
            stone_map[stone] = 0
        stone_map[stone] += 1

    return stone_map


def blink(stones: Dict[str, int]):
    local = stones.copy()
    for stone, count in local.items():
        if count == 0:
            del stones[stone]
            continue
        if stone == "0":
            if not stones.get("1", None):
                stones["1"] = 0
            stones["1"] += count
            stones[stone] -= count
            continue

        length = len(stone)
        if length % 2 == 0:
            left_stone = stone[:(length // 2)]
            right_stone = str(int(stone[(length // 2):]))
            if not stones.get(left_stone, None):
                stones[left_stone] = 0
            if not stones.get(right_stone, None):
                stones[right_stone] = 0

            stones[left_stone] += count
            stones[right_stone] += count
            stones[stone] -= count
        else:
            stone_value = str(int(stone) * 2024)
            if not stones.get(stone_value, None):
                stones[stone_value] = 0
            stones[stone_value] += count
            stones[stone] -= count

        if stones[stone] == 0:
            del stones[stone]

    return stones


def process_blinks(stones: Dict[str, int], blinks: int):
    for i in range(blinks):
        stones = blink(stones)

    return stones


initial_stones = get_inital_data('day11.input')
final_stones_a = process_blinks(initial_stones, 25)
total_a = 0
for count in final_stones_a.values():
    total_a += count
print("Part A:", total_a)

final_stones_b = process_blinks(initial_stones, 75)
total_b = 0
for count in final_stones_b.values():
    total_b += count
print("Part B:", total_b)


