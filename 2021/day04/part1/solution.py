from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)


def sum_card(card, lastnum):
  sum: int = 0
  for y in range(5):
    for x in range(5):
      value = card[y][x]
      if type(value) == type(2021041):  # If the value is a number (not an "X")
        sum += value
  return sum * lastnum


def check_win_one_col(card, col):
  for y in range(5):
    if not card[y][col] == "X":
      return False
  return True


def check_win_col(card):
  for x in range(5):
    if check_win_one_col(card, x):
      return True
  return False


def check_win_row(card):
  for y in range(5):
    if card[y] == ["X", "X", "X", "X", "X"]:
      return True
  return False


def check_win(card):
  return check_win_col(card) or check_win_row(card)


LOGGER.tee("Reading input...")
with open(INPUT_PATH, "r") as input_file:
  input_paragraphs: [str] = input_file.read().strip().split("\n\n")
bingo_numbers: int = [int(x) for x in input_paragraphs.pop(0).split(",")]
input_cards: [str] = input_paragraphs

bingo_cards: [[[int]]] = []
for input_card in input_cards:
  card: [[int]] = []
  for input_line in input_card.split("\n"):
    line = input_line.split(" ")
    # Remove extra spaces in the lines
    while "" in line:
      line.remove("")
    # Add the finished line to the card
    card.append([int(x) for x in line])
  # Save the finished card
  bingo_cards.append(card)
LOGGER.tee(f"Loaded {len(bingo_numbers)} numbers and {len(bingo_cards)} cards.")

LOGGER.tee()

LOGGER.tee("Playing the game...")
LOGGER.indent()
for number in tqdm(bingo_numbers):
  LOGGER.log(f"Processing number {number}")
  LOGGER.indent()
  for card_inx, card in enumerate(bingo_cards):
    LOGGER.log(f"Processing card {card_inx}")
    LOGGER.indent()
    for line_inx, line in enumerate(card):
      try:
        bingo_cards[card_inx][line_inx][line.index(number)] = "X"
        LOGGER.log("Ticking number.")
      except ValueError:
        pass
    LOGGER.unindent()
  
  # Check if any card won
  for card_inx, card in enumerate(bingo_cards):
    if check_win(card):
      LOGGER.tee(f"Card {card_inx} won. Score: {sum_card(card, number)}")
      LOGGER.dump_log()  # Write output file
      exit(0)
  LOGGER.unindent()
LOGGER.unindent()

# Write logs to output file
# This will only trigger if somehow no card would have won, ever
LOGGER.dump_log()
