from tqdm import tqdm

input_path = "day_four.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_passports = input_string.split("\n\n")

output_path = "part_one.out"
output_string = ""


def save_output(exit_code: int):
    global output_path
    global output_string

    output_file = open(output_path, "w")
    output_file.write(output_string)
    output_file.close()

    exit(exit_code)


def l_print(what: str):
    global output_string
    output_string += what + "\n"


required_fields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"  # ,
    # "cid"  # declared optional by part_one
]


number_of_valids = 0
for passport in tqdm(input_passports):
    index = input_passports.index(passport)
    passport = passport.replace("\n", " ")

    valid = True
    for field in required_fields:
        if passport.find(field) == -1:
            valid = False
            l_print(f"{index+1:0>3}.: Missing {field}")

    if valid:
        number_of_valids += 1
        l_print(f"{index+1:0>3}.:   Valid")
    else:
        l_print(f"{index+1:0>3}.: Invalid")
    l_print("")

l_print(f"Validated a total of {len(input_passports)} passports, of which {number_of_valids} were valid!")
save_output(0)
