from tqdm import tqdm

input_path: str = "day_six.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_groups: [str] = input_string.split("\n\n")

output_path = "part_one.out"
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


total_yeses: int = 0
for group in tqdm(input_groups):
    g_index: int = input_groups.index(group)
    l_print(f"Processing group {g_index+1:0>3}")
    people: [str] = group.split("\n")
    group_yeses: [str] = []

    p_index: int = 0
    for person in people:
        l_print(f"Processing person {p_index+1}:")

        for question in person:
            if question not in group_yeses:
                group_yeses.append(question)
                l_print(f"Question {question} answered positive by person {p_index+1}!")
            else:
                l_print(f"Skipping {question}: answered positive already!")

        p_index += 1

    group_yes_amount: int = len(group_yeses)
    total_yeses += group_yes_amount
    l_print(f"Finished processing group {g_index+1:0>3}!")
    l_print(f"Questions answered positive: {group_yeses}")
    l_print(f"{total_yeses - group_yes_amount} + {group_yes_amount} = {total_yeses}")
    l_print()
    l_print()
l_print()
l_print(f"In total, {total_yeses} questions were answered positive group-uniquely.")

save_output(0)
