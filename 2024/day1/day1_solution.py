from collections import Counter

with open("day1.input") as input:
    text_input = input.read()

left_list = []
right_list = []
for line in text_input.split("\n"):
     [left, right] = [int(x.strip()) for x in line.split(" ") if x]
     left_list.append(left)
     right_list.append(right)

left_list.sort()
right_list.sort()
distance = 0
for i in range(len(left_list)):
    distance += abs(right_list[i] - left_list[i])

print("distance:",distance)

counter = Counter(right_list)
similarity = 0
for n in left_list:
    similarity += n * counter[n]

print("similarity:", similarity)
