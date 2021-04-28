from tqdm import tqdm

input_path: str = "day_six.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_groups: [str] = input_string.split("\n\n")

output_path = "part_two.out"
output_string = ""


def save_output(exit_code: int):
    global output_path
    global output_string

    print("Saving output file...")
    with open(output_path, "w") as output_file:
        output_file.write(output_string)
    print("Done! Exiting...")

    exit(exit_code)


def l_print(what: str = ""):
    global output_string
    output_string += what + "\n"


def pre_process_group(group_string: str) -> [str]:
    global input_groups

    questions: [str] = []
    people: [str] = group_string.split("\n")
    for person in people:
        for question in person:
            if question not in questions:
                questions.append(question)
            # else:
                # Question was already added to the list - don't add again

    return questions


def process_group(group_string: str, questions: [str]) -> [str]:
    global input_groups

    group_lines = len(group_string.split("\n"))

    unanimous: [str] = []
    for char in questions:
        if group_string.count(char) == group_lines:
            unanimous.append(char)

    return unanimous  # Return remaining questions


total_unanimous: int = 0
for group in tqdm(input_groups):
    g_index = input_groups.index(group)

    l_print(f"{g_index}.: Pre-Processing...")
    all_questions: [str] = pre_process_group(group)
    l_print(f"{g_index}.: Finished preprocessing - total questions:")
    l_print(f"[{len(all_questions)}]: {all_questions}")
    l_print(f"{g_index}.: Post-Processing...")
    unanimous_questions: [str] = process_group(group, all_questions)
    group_unanimous = len(unanimous_questions)
    l_print(f"{g_index}.: Finished postprocessing - unanimous questions:")
    l_print(f"[{group_unanimous}]: {unanimous_questions}")
    total_unanimous += group_unanimous
    l_print(f"(Total: {total_unanimous - group_unanimous} + {group_unanimous} = {total_unanimous})")
    l_print()
    l_print()

l_print(f"{total_unanimous} questions were answered group-uniquely and group-unanimously!")
save_output(0)
