import re


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


times: list[int] = get_values("time")
dists: list[int] = get_values("distance")

solution: int = 1
for race_inx in range(len(times)):
    winning_windups: int = 0
    race_time: int = times[race_inx]
    record_dist: int = dists[race_inx]

    for windup in range(race_time):
        reached_dist: int = calculate_distance(windup, race_time)
        if reached_dist > record_dist:
            winning_windups += 1
    solution *= winning_windups
print(f"SOLVE: {solution}")
