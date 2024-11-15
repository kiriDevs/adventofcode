use std::fs;

fn read_input(filename: &str) -> String {
    if let Ok(input_text) = fs::read_to_string(filename) {
        match input_text.trim().split("\n").next() {
            Some(input_text) => input_text.to_owned(),
            None => panic!("Read invalid input from file: {}", filename),
        }
    } else {
        panic!("Unable to read input from file: {}", filename);
    }
}

fn main() {
    let input: String = read_input("day01.in");

    let mut current_floor: i16 = 0; // = part1 solution
    let mut first_basement_step: u16 = 0; // = part2 solution

    let mut input_chars = input.chars();
    let mut char_inx: u16 = 0;
    loop {
        match input_chars.next() {
            Some(char) => {
                current_floor += match char {
                    '(' => 1,
                    ')' => -1,
                    _ => panic!("Invalid character in input!")
                };

                if first_basement_step == 0 && current_floor < 0 {
                    first_basement_step = char_inx + 1;
                }
            },
            None => { break; }
        }
        char_inx += 1;
    }

    if first_basement_step == 0 {
        panic!("No first basement step");
    }
    
    println!("Part 1: {}", current_floor);
    println!("Part 2: {}", first_basement_step);
}
