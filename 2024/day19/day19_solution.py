from typing import List


def aoc19(filename):
    with open(filename) as input_data:
        data = input_data.read().split("\n\n")
        patterns = data[0].split(", ")
        towels = data[1].split("\n")

        patterns.sort(key= lambda x: len(x), reverse=True)

    DP = {}
    def ways_to_make_towel(towel:str, patterns: List[str]):
        if towel in DP:
            return DP[towel]
        ans = 0
        if not towel:
            ans = 1
        for pattern in patterns:
            if towel.startswith(pattern):
                ans += ways_to_make_towel(towel[len(pattern):], patterns)
        DP[towel] = ans
        return ans

    def partA():
        count = 0
        for towel in towels:
            if ways_to_make_towel(towel, patterns):
                count += 1
        return count

    def partB():
        count = 0
        for towel in towels:
            count += ways_to_make_towel(towel, patterns)
        return count



    print(partA())
    print(partB())




aoc19('day19.input')
