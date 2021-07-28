# Import external modules
from tqdm import tqdm
from typing import List, Union

# Let's define our target.
TARGET_BAG: str = "shiny gold"

# Define logging features
OUTPUT_PATH: str = "part_two.out"
LOG: List[str] = []
LOG_INDENT: int = 0
INDENT_STEPS: int = 2


def indent():
    global LOG_INDENT
    global INDENT_STEPS

    LOG_INDENT += INDENT_STEPS


def unindent():
    global LOG_INDENT
    global INDENT_STEPS

    LOG_INDENT -= INDENT_STEPS


def get_indent():
    global LOG_INDENT

    indent: str = ""
    for _ in range(LOG_INDENT):
        indent += " "
    return indent


def indented_print(what: str = ""):
    if type(what) is not str:
        what = str(what)

    print(get_indent() + what)


def log(what: str = ""):
    global LOG

    if type(what) is not str:
        what = str(what)

    LOG.append(get_indent() + what)


def print_log(what: str = ""):
    indented_print(what)
    log(what)


def save_log():
    global LOG

    output_string = "\n".join(LOG)
    with open(OUTPUT_PATH, "w") as output_file:
        output_file.write(output_string)

    print(f"Successfully wrote log to {OUTPUT_PATH}.")


# Define classes to make this whole thing easier
class BagManager:
    def __init__(self):
        self.bag_registry: dict = {}

    def register_bag(self, name, obj):
        self.bag_registry[name] = obj

    def get_bag(self, name):
        return self.bag_registry[name]

    def count_registered_bags(self):
        return len(self.bag_registry.keys())


class Bag:
    def __init__(self, name: str, tree: dict):
        self.name: str = name
        self.tree: dict = tree

        self.worth: Union[int, None] = None

    def self_register(self):
        BAG_MANAGER.register_bag(self.name, self)

    def calculate_worth(self) -> int:
        my_worth: int = 1
        for child_name in self.tree.keys():
            child_amount = self.tree[child_name]
            child_object = BAG_MANAGER.get_bag(child_name)
            child_weight = child_object.get_worth()
            my_worth += child_amount * child_weight
        return my_worth

    def get_worth(self) -> int:
        if self.worth is None:
            log(f"{self.name}: Re-Calculating worth...")
            indent()
            self.worth = self.calculate_worth()
            unindent()
            log(f"{self.name}: Done. [{self.worth}]")
        else:
            log(f"{self.name}: Providing cached worth. [{self.worth}]")

        return self.worth


# Define a global bag manager
BAG_MANAGER: BagManager = BagManager()

# Read our input
INPUT_PATH: str = "day07.in"
with open(INPUT_PATH, "r") as input_file:
    raw_input = input_file.read()
INPUT_LINES = raw_input.split("\n")
print_log(f"Read {len(INPUT_LINES)} lines from {INPUT_PATH}.")

# Remove empty lines from INPUT_LINES
print_log("Starting processing and cleaning input.")
indent()

deleted_lines: int = 0
for line_index in tqdm(range(len(INPUT_LINES))):
    # Check if we are already done because of previously deleted lines
    if line_index >= len(INPUT_LINES):
        break  # We are done

    input_line = INPUT_LINES[line_index]
    if len(input_line.strip()) == 0:
        log(f"Removing line {line_index+deleted_lines+1}: Empty.")
        del INPUT_LINES[line_index]
        deleted_lines += 1

unindent()
print_log(f"Left {len(INPUT_LINES)} lines intact.")
print_log()


# Create a function for parsing the lines to bags
def parse_input_line(line: str) -> Bag:
    segments: List[str] = line.split(" bags contain ")
    bag_color: str = segments[0]
    containments_string: str = segments[1]
    containments: List[str] = containments_string.split(", ")

    fitting_colors_amount: int
    if containments_string == "no other bags.":
        return Bag(bag_color, {})
    
    containment_tree: dict = {}
    for containment in containments:
        containment_parts = containment.split(" ")
        contain_amount = containment_parts[0]
        contain_color = f"{containment_parts[1]} {containment_parts[2]}"
        containment_tree[contain_color] = int(contain_amount)

        log(f"{contain_amount}x {contain_color}")

    return Bag(bag_color, containment_tree)


# Parse all the bags
parsed_bags: List[Bag] = []
for input_line in INPUT_LINES:
    log(input_line)
    indent()

    bag: Bag = parse_input_line(input_line)
    parsed_bags.append(bag)

    unindent()
    log("-> Parsed bag: " + str({"name": bag.name, "tree": bag.tree}))

# Register all the bags in the BagManager
print_log("Registering parsed bags...")

indent()
for bag in tqdm(parsed_bags):
   log(f"Registering '{bag.name}' bag.") 
   bag.self_register()
unindent()

registered_bags_count: int = BAG_MANAGER.count_registered_bags()
print_log(f"Successfully registered {registered_bags_count} bags.")

log()

target_worth: int = BAG_MANAGER.get_bag("shiny gold").get_worth()
target_contains: int = target_worth - 1

print_log()
print_log(f"The target ({TARGET_BAG}) has a worth of {target_worth}.")
print_log(f"Therefore, one {TARGET_BAG} bag contains {target_contains} bags.")
print_log()

save_log()
