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

winning_windups: int = 0
for windup in tqdm(range(time)):
    reached_dist: int = calculate_distance(windup, time)
    if reached_dist > dist:
        winning_windups += 1
print(f"SOLVE: {winning_windups}")
