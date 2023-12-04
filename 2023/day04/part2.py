with open("input", "r") as input_file:
    input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]

card_map: dict[int, (list[int], list[int])] = {}
for input_line in input_lines:
    id_part, card = input_line.split(": ")
    card_id = int(id_part.split()[1])

    winner_str, owned_str = card.split(" | ")
    winners: [int] = [int(a) for a in winner_str.split()]
    owneds: [int] = [int(a) for a in owned_str.split()]

    card_map[card_id] = (winners, owneds)

win_map: dict[int, list[int]] = {}
for card_id in card_map.keys():
    card: ([int], [int]) = card_map[card_id]

    winnerc: int = 0
    for winning in card[0]:
        if winning in card[1]:
            winnerc += 1

    won_clones: [int] = []
    for i in range(winnerc):
        won_clones.append(card_id + i + 1)
    win_map[card_id] = won_clones

owned_cards: dict[int, int] = dict([(i, 1) for i in card_map.keys()])
for card_id in card_map.keys():
    for won_clone_id in win_map[card_id]:
        owned_cards[won_clone_id] += owned_cards[card_id]

solution: int = sum(owned_cards.values())
print(f"SOLVE: {solution}")
