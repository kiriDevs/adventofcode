from tqdm import tqdm

input_path = "day_five.in"
input_file = open(input_path, "r")
input_string = input_file.read()
input_file.close()
input_boarding_passes = input_string.split("\n")

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


seat_ids = []
highest_seat_id = None
for boarding_pass in tqdm(input_boarding_passes):
    index = input_boarding_passes.index(boarding_pass)

    rowCode = boarding_pass[0:7]
    colCode = boarding_pass[7:10]

    bin_row_code = ""
    for rowChar in rowCode:
        if rowChar is "F":
            bin_row_code += "0"
        elif rowChar is "B":
            bin_row_code += "1"
        else:
            l_print("")
            l_print(f"{index + 1:0>3}.: ERROR: Invalid char in rowCode: {rowChar}")
            save_output(1)
    row = int(bin_row_code, 2)

    bin_col_code = ""
    for colChar in colCode:
        if colChar is "L":
            bin_col_code += "0"
        elif colChar is "R":
            bin_col_code += "1"
        else:
            l_print("")
            l_print(f"{index + 1:0>3}.: ERROR: Invalid char in colCode: {colChar}")
    col = int(bin_col_code, 2)

    seat_id = (8 * row) + col

    if index is 0:
        highest_seat_id = seat_id
    else:
        highest_seat_id = max(highest_seat_id, seat_id)

    seat_ids.append(seat_id)
    l_print(f"{index + 1:0>3}.: Row: {row:0>3} Col: {col} - ID: {seat_id:0>3}")

l_print("")
l_print(f"Checked {len(input_boarding_passes)} boarding passes. The highest seat id was {highest_seat_id}.")
l_print("")

# Check for own seat: ID is missing on boarded list, ID+1 and ID-1 exist though
possible_hits = []
for my_seat_id_candidate in tqdm(range(0, highest_seat_id)):
    if my_seat_id_candidate in seat_ids:
        l_print(f"Checked seat_id {my_seat_id_candidate:0>3}: Already checked in")
        continue

    if not ((my_seat_id_candidate - 1) in seat_ids):
        l_print(f"Checked seat_id {my_seat_id_candidate:0>3}: seat_id-1 doesn't exist")
        continue

    if not ((my_seat_id_candidate + 1) in seat_ids):
        l_print(f"Checked seat_id {my_seat_id_candidate:0>3}: seat_id+1 doesn't exist")
        continue

    l_print(f"Checked seat_id {my_seat_id_candidate:0>3}: Meeting criteria - probably my seat!")
    possible_hits.append(my_seat_id_candidate)

l_print("")
l_print(f"These seat_ids could be mine:")
l_print(f"{possible_hits}")
save_output(0)
