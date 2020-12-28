from tqdm import tqdm
from os import remove as delfile
from os.path import exists as file_exists
import yaml
import re

input_path = "day_four.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_passports = input_string.split("\n\n")

output_path = "part_two.out"
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

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
#           If cm, the number must be at least 150 and at most 193.
#           If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.

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
        passport = passport.replace(" ", "\n")
        passport = passport.replace(":", ": ")
        temp_file = open("tmp", "w")
        temp_file.write(passport)
        temp_file.close()
        temp_file = open("tmp", "r")
        data = yaml.safe_load(temp_file)
        temp_file.close()

        # Check birth year
        if (data["byr"] < 1920) or (data["byr"] > 2002):
            valid = False
            l_print(f"{index+1:0>3}.: Invalid Birth Year")

        # Check issue year
        if (data["iyr"] < 2010) or (data["iyr"] > 2020):
            valid = False
            l_print(f"{index+1:0>3}.: Invalid Issue Year")

        # Check expiry year
        if (data["eyr"] < 2020) or (data["eyr"] > 2030):
            valid = False
            l_print(f"{index+1:0>3}.: Invalid Expiration Year")

        # Check height
        if type(data["hgt"]) is int:
            valid = False
            l_print(f"{index + 1:0>3}.: Invalid Height")
        else:
            if data["hgt"].endswith("cm"):
                data["hgt"] = int(data["hgt"].split("cm")[0])
                if (data["hgt"] < 150) or (data["hgt"] > 193):
                    valid = False
                    l_print(f"{index+1:0>3}.: Invalid Height")
            elif data["hgt"].endswith("in"):
                data["hgt"] = int(data["hgt"].split("in")[0])
                if (data["hgt"] < 59) or (data["hgt"] > 76):
                    valid = False
                    l_print(f"{index + 1:0>3}.: Invalid Height")
            else:
                valid = False
                l_print(f"{index+1:0>3}.: Invalid Height")

        # Check hair color
        if not (re.search("hcl: #......", passport)):
            valid = False
            l_print(f"{index+1:0>3}.: Invalid Hair Color")

        # Check eye color
        if not (data["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]):
            valid = False
            l_print(f"{index + 1:0>3}.: Invalid Eye color")

        # Check passport id
        if not (len(str(data["pid"])) is 9):
            valid = False
            l_print(f"{index + 1:0>3}.: Invalid Passport ID")

        try:
            int(data["pid"])
        except ValueError:
            valid = False
            l_print(f"{index + 1:0>3}.: Invalid Passport ID")
        except TypeError:
            valid = False
            l_print(f"{index + 1:0>3}.: Invalid Passport ID")

    if valid:
        number_of_valids += 1
        l_print(f"{index+1:0>3}.:   Valid")
    else:
        l_print(f"{index+1:0>3}.: Invalid")
    l_print("")


if file_exists("tmp"):
    delfile("tmp")

l_print(f"Validated a total of {len(input_passports)}, of which {number_of_valids} were valid!")
save_output(0)
