from tqdm import tqdm

input_path = "day_two.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_data = input_string.split("\n")

output_path = "part_two.out"
output_string = ""


def save_output(exit_code):
    global output_path
    global output_string

    output_file = open(output_path, "w")
    output_file.write(output_string)
    output_file.close()

    exit(exit_code)


valid_passwords = 0
for entry in tqdm(input_data):
    fields = entry.split(": ")
    policy = fields[0]
    password = fields[1]

    policy_parts = policy.split(" ")
    numbers = policy_parts[0]
    char = policy_parts[1]

    places = numbers.split("-")
    firstPlace = int(places[0])
    secondPlace = int(places[1])

    firstIndex = firstPlace - 1
    secondIndex = secondPlace - 1

    firstPlaceOkay = password[firstIndex] == char
    secondPlaceOkay = password[secondIndex] == char

    if (firstPlaceOkay or secondPlaceOkay) and (not (firstPlaceOkay and secondPlaceOkay)):
        output_string += f"  Valid: {password}" + "\n"
        valid_passwords += 1
    else:
        output_string += f"Invalid: {password}" + "\n"
output_string += "\n" + f"Found {valid_passwords} valid passwords!" + "\n"
save_output(0)

