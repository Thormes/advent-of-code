from typing import List, Optional


def get_files_spaces(data: str) -> tuple[List[int], List[int]]:
    files = []
    free_space = []
    for i in range(len(data)):
        if i % 2 == 0:
            files.append(int(data[i]))
        else:
            free_space.append(int(data[i]))

    return files, free_space


def get_fragment_string(files: list[int], spaces: list[int]) -> list[int]:
    filesystem = []
    for i in range(len(files)):
        filesystem += [i] * files[i]
        if i < len(spaces):
            filesystem += '.' * spaces[i]
    return filesystem


def defrag_file_system_a(content: list):
    left = 0
    right = len(content) - 1
    while left < right:
        while content[right] == '.':
            right -= 1

        while content[right] != '.':
            while content[left] != '.':
                left += 1

            if left >= right:
                break
            content[left] = content[right]
            content[right] = '.'
            right -= 1

    return content


def get_next_free_space(content: list, limit: int, size: int) -> Optional[int]:
    count = 0
    pos = 0
    for i in range(len(content)):
        if content[i] == '.':
            count += 1
        else:
            count = 0
            pos = i + 1

        if count == size and pos < limit:
            return pos

    return None


def defrag_file_system_b(content: list):
    right = len(content) - 1
    free_spaces = map_free_spaces(content)
    while 0 < right:
        size = 0
        while content[right] == '.':
            right -= 1

        #calculate size to move, moving the right pointer
        last_digit = content[right]
        while content[right] == last_digit:
            right -= 1
            size += 1

        #find next free size slot
        slot = get_next_free_space_b(free_spaces, size, right)

        #if found free space, move the file
        if slot:
            for i in range(size):
                content[slot + i] = content[right + 1 + i]
                content[right + 1 + i] = '.'
    return content

def get_next_free_space_b(free_map: dict[int, int], size: int, pos_id) -> Optional[int]:
    for key in sorted(free_map.keys()):
        free_map[key] = free_map.pop(key)
    for pos, free_space in free_map.items():
        if free_space >= size and pos < pos_id:
            free_map[pos + size] = free_map[pos] - size
            del free_map[pos]
            return pos

    return None

def map_free_spaces(content: list):
    spaces = {}
    count = 0
    pos = 0
    for i in range(len(content)):
        if content[i] == '.':
            count += 1
        else:
            if count > 0:
                spaces[pos] = count
            count = 0
            pos = i + 1

    return spaces

def checksum(files: list, skip_free: bool) -> int:
    total = 0
    for i in range(len(files)):
        if files[i] == '.' and skip_free:
            break
        elif files[i] == '.':
            continue
        total += i * files[i]
    return total


def get_response_a(filename: str):
    with open(filename) as text_input:
        input_string = text_input.read().strip()
    files_list, free_spaces = get_files_spaces(input_string)
    filesystem = get_fragment_string(files_list, free_spaces)
    defragment = defrag_file_system_a(filesystem)
    files_checksum = checksum(defragment, True)
    return files_checksum


def get_response_b(filename: str):
    with open(filename) as text_input:
        input_string = text_input.read().strip()
    files_list, free_spaces = get_files_spaces(input_string)
    filesystem = get_fragment_string(files_list, free_spaces)
    defragment = defrag_file_system_b(filesystem)
    files_checksum = checksum(defragment, False)
    return files_checksum


print(get_response_b("day9.input"))
