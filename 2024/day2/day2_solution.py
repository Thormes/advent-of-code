lists = []


def safe(lista: list[int]):
    direction = 1 if lista[1] > lista[0] else 0 if lista[1] == lista[0] else -1
    last = lista[0]
    for i in range(1, len(lista)):
        diff = (lista[i] - last) * direction
        if diff > 3 or diff < 1:
            return False
        last = lista[i]
    return True


def test_dampen(lista):
    for i in range(len(lista)):
        new_list = lista.copy()
        new_list.pop(i)
        if safe(new_list):
            return True

    return False


with open("day2.input") as entry:
    lines = entry.readlines()
    for line in lines:
        lists.append([int(x) for x in line.split(" ") if x])

count = 0
for test in lists:
    if safe(test):
        count += 1
    elif test_dampen(test):
        count += 1

print(count)
