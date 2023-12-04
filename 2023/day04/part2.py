with open("input", "r") as input_file:
    input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]

# Parse the input into something like this: [card_id, (winning_numbers, owned_numbers)]
card_map: dict[int, (list[int], list[int])] = {}
for input_line in input_lines:
    id_part, card = input_line.split(": ")
    card_id = int(id_part.split()[1])

    winner_str, owned_str = card.split(" | ")
    winners: [int] = [int(a) for a in winner_str.split()]
    owneds: [int] = [int(a) for a in owned_str.split()]

    card_map[card_id] = (winners, owneds)

# For each card type, pre-calculate which other card types it will win
win_map: dict[int, list[int]] = {}
for card_id in card_map.keys():
    card: ([int], [int]) = card_map[card_id]

    # Count how many wins we have on this card in total
    winnerc: int = 0
    for winning in card[0]:
        if winning in card[1]:
            winnerc += 1

    # Count through the list to see what exact cards are won
    won_clones: [int] = []
    for i in range(winnerc):
        won_clones.append(card_id + i + 1)
    win_map[card_id] = won_clones

# We start with one of each card
owned_cards: dict[int, int] = dict([(i, 1) for i in card_map.keys()])
# Iterate through all card types to calculate how many copies we own
for card_id in card_map.keys():
    for won_clone_id in win_map[card_id]:
        owned_cards[won_clone_id] += owned_cards[card_id]

# The solution is the total amount of cards
solution: int = sum(owned_cards.values())
print(f"SOLVE: {solution}")
