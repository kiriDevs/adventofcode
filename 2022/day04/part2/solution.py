INPUT_PATH: str = "../input"

with open(INPUT_PATH, "r") as file_name:
    raw_comparisons: [str] = file_name.read().strip().split("\n")

comparisons: [[str]] = [a.split(",") for a in raw_comparisons]

solution: int = 0
for comparison in comparisons:
    ranges: [[int]] = []
    for assignment in comparison:
        bounds = assignment.split("-")
        ranges.append(list(range(int(bounds[0]), int(bounds[1])+1)))

    overlaps: bool = False
    for a in ranges[0]:
        if a in ranges[1]:
            overlaps = True
    if overlaps:
        solution += 1

print(solution)
