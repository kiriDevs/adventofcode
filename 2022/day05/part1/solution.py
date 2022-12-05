INPUT_PATH: str = "../input"

with open(INPUT_PATH, "r") as input_file:
    input_data = input_file.read().split("\n\n")
starting_configuration_lines: [str] = input_data[0].split("\n")
instructions: [str] = input_data[1].strip().split("\n")

containers: [[str]] = [[] for i in range(9)]
for line in starting_configuration_lines:
    cur_col: int = 0
    while cur_col <= 8:
        char_inx: int = cur_col * 3 + cur_col
        char: str = line[char_inx]
        print(char)
        if char == "[":
            next_char: str = line[char_inx +1]
            containers[cur_col].append(next_char)
        elif char in "123456789":
            break
        cur_col += 1

for instruction in instructions:
    parts: [str] = instruction.split(" ")
    amount: int = int(parts[1])
    from_stack: int = int(parts[3]) -1
    to_stack: int = int(parts[5]) -1
    
    for i in range(amount):
        taken: str = containers[from_stack].pop(0)
        containers[to_stack].insert(0, taken)

print("".join([c[0] for c in containers]))
