QUESTION_BAG: dict[str, int] = {"red": 12, "green": 13, "blue": 14}


def is_set_possible(set: [dict[str, int]]) -> bool:
    for color in set.keys():
        cube_amount: int = set[color]
        if cube_amount > QUESTION_BAG.get(color, 0):
            return False
    return True


def is_game_possible(game: list[dict[str, int]]) -> bool:
    for set in game:
        if not is_set_possible(set):
            return False
    return True


with open("./example.input", "r") as input_file:
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
    if is_game_possible(game):
        solution += game_id
print(f"SOLVE: {solution}")
