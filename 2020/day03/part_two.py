from tqdm import tqdm

input_path = "day_three.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_rows = input_string.split("\n")

output_path = "part_two.out"
output_string = ""


def save_output(exit_code):
    global output_path
    global output_string

    output_file = open(output_path, "w")
    output_file.write(output_string)
    output_file.close()

    exit(exit_code)


max_x = len(input_rows[0])
max_y = len(input_rows)


def has_tree(check_x, check_y) -> bool:
    global output_string

    output_string += f"Checking ({check_x:0>2}|{check_y:0>3}) - Tree: "
    result = input_rows[check_y]
    result = result[check_x] == "#"
    output_string += f"{result}" + "\n"

    return result


def trace_path(slope_to_trace) -> int:
    global max_x
    global max_y
    global output_string

    scan_increments = slope_to_trace.split(".")
    scan_increment_x = int(scan_increments[0])
    scan_increment_y = int(scan_increments[1])

    y = 0
    trees = 0
    while y < max_y:
        x = (y * scan_increment_x) % max_x

        if has_tree(x, y):
            trees += 1

        y += scan_increment_y
    return trees


slopes = ["1.1", "3.1", "5.1", "7.1", "1.2"]
trees_hit = {}
for slope in tqdm(slopes):
    slope_coords = slope.split(".")
    slope_x = slope_coords[0]
    slope_y = slope_coords[1]

    output_string += f"Tracing path for slope: {slope_x} right, {slope_y} down" + "\n"
    trees_hit[slope] = trace_path(slope)
    output_string += f"Encountered a total of {trees_hit[slope]} trees on the way down!" + "\n" + "\n"

output_string += "\n" + "\n" + "\n"

product_of_trees_hit = 1
tree_hit_numbers = []
for slope in slopes:
    output_string += f"Slope \"{slope}\" hit {trees_hit[slope]} trees!" + "\n"
    tree_hit_numbers.append(trees_hit[slope])
    product_of_trees_hit *= trees_hit[slope]

output_string += "\n" + f"The product of the total numbers of trees hit is {product_of_trees_hit}!"
save_output(0)
