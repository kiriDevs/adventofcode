from tqdm import tqdm

input_path = "day_one.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_strings = input_string.split("\n")

output_path = "part_two.out"
output_string = ""


def save_output(output_code):
    global output_path
    global output_string

    output_file = open(output_path, "w")
    output_file.write(output_string)
    output_file.close()

    exit(output_code)


input_numbers = []
output_string += "Indexing numbers..." + "\n"
for string in input_strings:
    input_numbers.append(int(string))
    output_string += string + "\n"
output_string += "Finished indexing numbers - trying combinations to find x + y + z (x + y + z = 2020)!" + "\n"
output_string += "\n"

for num1 in tqdm(input_numbers):
    for num2 in input_numbers:
        if (num1 + num2) >= 2020:
            output_string += f"{num1} + {num2} = {num1 + num2} ( > 2020) -> Skipping..." + "\n"
            continue  # Don't bother trying num3 if num1 + num2 is already too large

        for num3 in input_numbers:
            result = num1 + num2 + num3
            output_string += f"{num1} + {num2} + {num3} = {result}" + "\n"

            if result == 2020:
                output_string += f"FOUND: {num1} + {num2} + {num3} = {result}" + "\n"
                output_string += "\n"
                output_string += f"ANSWER: {num1} * {num2} * {num3} = {num1 * num2 * num3}" + "\n"
                save_output(0)
save_output(1)
