from tqdm import tqdm

input_path = "day_three.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_rows = input_string.split("\n")

output_path = "part_one.out"
output_string = ""


def save_output(exit_code):
    global output_path
    global output_string

    output_file = open(output_path, "w")
    output_file.write(output_string)
    output_file.close()

    exit(exit_code)


max_x = len(input_rows[0])
scan_increment_x = 3


def has_tree(check_x, check_y) -> bool:
    global output_string

    result = input_rows[check_y][check_x] == "#"
    output_string += f"Checking ({check_x:0>2}|{check_y:0>3}) - Tree: {result}" + "\n"

    return result


trees = 0
for y in tqdm(range(len(input_rows))):
    x = (y * scan_increment_x) % max_x

    if has_tree(x, y):
        trees += 1
output_string += "\n" + f"Encountered a total of {trees} trees on the way down!" + "\n"
save_output(0)
