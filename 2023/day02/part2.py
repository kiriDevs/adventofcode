def get_set_minimum(set: [dict[str, int]]) -> dict[str, int]:
    required: dict[str, int] = {}
    for color in set.keys():
        required[color] = max(required.get(color, 0), set[color])
    return required


def get_game_minimum(game: list[dict[str, int]]) -> dict[str, int]:
    required: dict[str, int] = {}
    for set in game:
        set_required = get_set_minimum(set)
        for color in set_required.keys():
            required[color] = max(required.get(color, 0), set_required[color])
    return required


with open("./input", "r") as input_file:
    input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]

game_map: dict[int, list[dict[str, int]]] = {}
for input_line in input_lines:
    line_parts: [str] = input_line.split(": ")
    game_id: int = int(line_parts[0].split(" ")[1])
    text_game_sets: [[str]] = [part.split(", ") for part in line_parts[1].split("; ")]

    game_sets: list[dict[str, int]] = []
    for text_game_set in text_game_sets:
        game_set: dict[str, int] = {}
        for set_element in text_game_set:
            parts: [str] = set_element.split(" ")
            amount: int = int(parts[0])
            color: str = parts[1]
            game_set[color] = amount
        game_sets.append(game_set)
    game_map[game_id] = game_sets

solution: int = 0
for game_id in game_map.keys():
    game: list[dict[str, int]] = game_map[game_id]
    game_required: dict[str, int] = get_game_minimum(game)

    game_power: int = 1
    for color in game_required.keys():
        game_power *= game_required[color]
    solution += game_power
print(f"SOLVE: {solution}")
