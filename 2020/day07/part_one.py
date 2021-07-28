# Import external modules
from tqdm import tqdm

# Declaring constants
OUTPUT_PATH: str = "part_one.out"
OUTPUT_STRING: str = ""
INPUT_PATH: str = "day07.in"
COLOR_TO_CONTAIN: str = "shiny gold" # The bag color we ultimately want to contain


# Declaring functions for logging while also writing to log
def printo(str = ""):
    global OUTPUT_STRING

    print(str)
    OUTPUT_STRING += f"{str}\n"


def log(str = ""):
    global OUTPUT_STRING

    OUTPUT_STRING += f"{str}\n"


# Reading input from input file
with open(INPUT_PATH, "r") as INPUT_FILE:
    INPUT_DATA: str = INPUT_FILE.read()

# Split input by rules (one rule per line)
input_rules: [str] = INPUT_DATA.split("\n")

# Declaring the dict that will store what can contain what
containment_tree: dict = {}

# Preprocessing: Removing (ignoring) empty lines
printo("Starting input pre-processing")
ignored_message: str = ""
for rule_index in tqdm(range(len(input_rules))):
    rule: str = input_rules[rule_index]
    if rule in ["", " "]:
        ignored_message += f"> Ignoring input line {rule_index+1:0>3}: Empty line" + "\n"
        del input_rules[rule_index] # Removing it from the array
printo("Finished pre-processing")
printo(ignored_message)

# Iterate through all the rules
printo("Building map of the different bag colors")
for rule_index in tqdm(range(len(input_rules))):
    rule: str = input_rules[rule_index]

    # Since we only want the colors, let's remove the bag parts
    rule: str = rule.replace("bags", "")
    rule: str = rule.replace("bag", "")

    # Remove the full stop at the end of the rule
    rule: str = rule.replace(".", "")

    # Sanitize punctuation due to removal of 'bag' and 'bags'
    rule: str = rule.replace("  ", " ")
    rule: str = rule.replace(" , ", ", ")

    # Split the rule into two parts
    rule_parts: [str] = rule.split(" contain ")
    container: str = rule_parts[0]
    containable_list: str = rule_parts[1]
    containable: [str] = containable_list.split(", ")

    # Iterating through the items to remove the possible amounts, as they aren't needed
    for containable_item_index in range(len(containable)):
        # Getting the current value
        containable_item: str = containable[containable_item_index]

        containable_item_parts: [str] = containable_item.split(" ", 1)
        containable_item_name: str = containable_item_parts[1]

        # Stripping potential trailing space off of color names
        containable_item_name = containable_item_name.strip()

        # Writing the altered value back
        containable[containable_item_index] = containable_item_name

    if containable == ["other"]: # 'other' from 'no other bags' remains
        containable = []

    containment_tree[container] = containable
    log(f"Rule {rule_index:0>3}: {container} -> {containable}")
printo("Finished color mapping")
printo()

# Finding paths to contain target
printo("Starting to find paths to contain the target")


def canContainTarget(what, indent):
    global COLOR_TO_CONTAIN
    global containment_tree

    containables: [str] = containment_tree[what]
    if COLOR_TO_CONTAIN in containables:
        return True
    else:
        subcontainment_possible: bool = False;
        for color in containables:
            if canContainTarget(color, indent+1):
                subcontainment_possible = True;
        return subcontainment_possible


containment_path_amount: int = 0
for color_index in tqdm(range(len(containment_tree.keys()))):
    color: str = list(containment_tree.keys())[color_index]
    can_contain: bool = canContainTarget(color, 0)

    if can_contain:
        containment_path_amount += 1

    string: str = f"{color} can contain {COLOR_TO_CONTAIN}: "
    string = f"{string}{can_contain}"
    log(string)
printo()
printo("Finished resolving containment paths.")
printo(f"Found paths: {containment_path_amount}")
printo()

# Writing output to output output file
with open(OUTPUT_PATH, "w") as OUTPUT_FILE:
    OUTPUT_FILE.write(OUTPUT_STRING)

print("==========")
print(f"Successfully written output to {OUTPUT_PATH}.")
