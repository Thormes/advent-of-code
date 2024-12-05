rules = []
updates = []
getUpdates = False


def valid_update(check_update: list[int], rules_set: list[list[int]]) -> bool:
    for rule in rules_set:
        before = rule[0]
        after = rule[1]
        #disregard rule if any page is not in update
        if before not in update or after not in update:
            continue

        idx_before = check_update.index(before)
        idx_after = check_update.index(after)
        if idx_before > idx_after:
            return False

    return True


def correct_update(update_check: list[int], rules_set: list[list[int]]) -> list[int]:
    valid_rules = []

    #get applicable rules
    for rule in rules_set:
        before = rule[0]
        after = rule[1]
        #disregard rule if any page is not in update
        if before not in update_check or after not in update_check:
            continue
        valid_rules.append(rule)

    #create a dictionary to get how many numbers comes after each other number
    afters = {}
    for rule in valid_rules:
        before = rule[0]
        after = rule[1]
        if not afters.get(before, None):
            afters[before] = []
        afters[before].append(after)

    new_order = []

    #order by the number of pages that comes after each page, in order to get the position of each page
    ordered = dict(sorted(afters.items(), key=lambda item: len(item[1]), reverse=True))
    for key in ordered.keys():
        new_order.append(key)
    new_order.append(ordered[list(ordered.keys())[-1]][0])

    return new_order


with open("day5.input") as text_input:
    lines = text_input.readlines()

for line in lines:
    line = line.strip()
    if line == '':
        getUpdates = True
        continue
    if not getUpdates:
        rules.append([int(x) for x in line.split("|")])
    else:
        updates.append([int(x) for x in line.split(",")])

total_correct = 0
total_incorrect = 0
for update in updates:
    if valid_update(update, rules):
        middle = update[(len(update) // 2)]
        total_correct += middle
    else:
        corrected_update = correct_update(update, rules)
        middle = corrected_update[(len(corrected_update) // 2)]
        total_incorrect += middle

print("correct:", total_correct)
print("incorrect:", total_incorrect)
