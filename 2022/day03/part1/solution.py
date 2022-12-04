INPUT_PATH: str = "../input"

with open(INPUT_PATH, "r") as input_file:
    raw_backpacks: [str] = input_file.read().strip().split("\n")


def splitPack(pack: str) -> (str, str):
    mid: int = int(len(pack) / 2)

    first: str = pack[:mid]
    second: str = pack[mid:]
    return (first, second)


def getPriority(item: str) -> int:
    if item == item.lower():
        return ord(item) - 96
    elif item == item.upper():
        return ord(item) - 38
    else:
        return -1


backpacks: [(str, str)] = [splitPack(a) for a in raw_backpacks]
solution: int = 0
for backpack in backpacks:
    try:
        overlap: str = ""
        for item in backpack[0]:
            if item in backpack[1]:
                overlap = item
                raise StopIteration  # Why doesn't python have labeled loops?
    except:
        pass  # just continue with the next iteration
    solution += getPriority(overlap)
print(solution)
