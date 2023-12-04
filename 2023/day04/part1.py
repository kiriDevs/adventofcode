with open("input", "r") as input_file:
    input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]

score: int = 0
for input_line in input_lines:
    card = input_line.split(": ")[1]
    winner_str, owned_str = card.split(" | ")
    winners: [int] = [int(a) for a in winner_str.split()]
    owneds: [int] = [int(a) for a in owned_str.split()]

    winner_count: int = 0
    for owned in owneds:
        if owned in winners:
            winner_count += 1
    if winner_count > 0:
        score += pow(2, winner_count - 1)
print(f"SOLVE: {score}")
