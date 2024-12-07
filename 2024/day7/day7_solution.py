import itertools

cases = []
def get_case(line: str):
    line = line.strip()
    result, numbers = line.split(": ")
    return {"result": int(result), "numbers": [int(x) for x in numbers.split(" ")]}

def generate_combinations(numbers:list[int], partB: bool):
    operations = ['+', '*']
    if(partB):
        operations.append('||')
    num_operations = len(numbers) - 1
    combinations = list(itertools.product(operations, repeat=num_operations))
    results = []
    for combination in combinations:
        nums = numbers.copy()
        for i, operation in enumerate(combination):
            if operation == '+':
                nums[i+1] = nums[i] + nums[i+1]
            elif operation == '*':
                nums[i+1] = nums[i] * nums[i+1]
            else:
                nums[i+1] = int(str(nums[i]) + str(nums[i+1]))
        results.append({
            "operation": combination,
            "result": nums[-1]
        })

    return results


with open("day7.input") as text_input:
    for line in text_input.readlines():
        cases.append(get_case(line))


totalA = 0
totalB = 0
for case in cases:
    resultsA = generate_combinations(case["numbers"], False)
    resultsB = generate_combinations(case["numbers"], True)
    for result in resultsA:
        if result['result'] == case['result']:
            totalA += result['result']
            break
    for result in resultsB:
        if result['result'] == case['result']:
            totalB += result['result']
            break


print("Part A:",totalA)
print("Part B:",totalB)


