INPUT_PATH: str = "../input"

with open(INPUT_PATH, "r") as input_file:
    backpacks: [str] = input_file.read().strip().split("\n")


def get_priority(item: str) -> int:
    if item == item.lower():
        return ord(item) - 96
    elif item == item.upper():
        return ord(item) - 38
    else:
        return -1


def group(items: [str], per_group: int = 3) -> [[str]]:
    result: [[str]] = []

    cur_group: [str] = []
    for item in items:
        cur_group.append(item)
        if len(cur_group) == per_group:
            result.append(cur_group)
            cur_group = []

    return result


def find_overlap(group: [[str]]) -> str:
    candidates: [str] = list(group[0])
    extra_packs: [str] = group[1:]

    for item in candidates.copy():
        if item not in candidates:
            continue
        try:
            for pack in extra_packs:
                if item not in pack:
                    candidates.remove(item)
                    raise StopIteration
        except StopIteration:
            pass
    return candidates


overlaps: [str] = [find_overlap(group)[0] for group in group(backpacks)]
overlap_priorities: int = [get_priority(a) for a in overlaps]
solution: int = sum(overlap_priorities)

print(solution)
