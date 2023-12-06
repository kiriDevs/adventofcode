import re
from tqdm import tqdm


BASE_REGEX: str = "$$n$$: ([\\s\\d]*)"

with open("input", "r") as input_file:
    input_text: str = input_file.read().strip()


def get_values(line_name: str) -> list[int]:
    global input_text
    regex: str = BASE_REGEX.replace("$$n$$", line_name.capitalize())
    search: re.Match = re.search(regex, input_text)
    result: str = search.groups()[0].split()
    return [int(n) for n in result]


def calculate_distance(windup: int, total: int):
    # speed[mm/ms] = windup[ms]
    runtime: int = total - windup  # [ms]
    return runtime * windup  # [mm]


time: int = int("".join([str(t) for t in get_values("time")]))
dist: int = int("".join([str(d) for d in get_values("distance")]))


def is_winning(windup: int) -> bool:
    global time
    global dist
    return calculate_distance(windup, time) > dist


lowest: int = 0
while not is_winning(lowest):
    lowest += 1
print(f"Lowest: {lowest}")

highest: int = time
while not is_winning(highest):
    highest -= 1
print(f"Highest: {highest}")

solution: int = highest - lowest + 1
print(f"SOLVE: {solution}")
