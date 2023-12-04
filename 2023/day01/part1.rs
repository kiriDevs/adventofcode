use std::convert::TryInto;
use std::fs;

pub fn read_input(filename: &str) -> Vec<String> {
    if let Ok(input_text) = fs::read_to_string(filename) {
        input_text
            .trim()
            .split("\n")
            .map(|line| line.trim().to_owned())
            .collect()
    } else {
        panic!("Unable to read input from file: {}", filename);
    }
}

pub fn get_digits(line: &String) -> (usize, usize) {
    let mut chars = line.chars();
    let first: usize = {
        loop {
            match chars.nth(0) {
                Some(char) => {
                    if let Some(digit) = char.to_digit(10) {
                        break digit.try_into().unwrap();
                    }
                }
                None => panic!("Line has no digit?"),
            }
        }
    };

    chars = line.chars();
    let last: usize = {
        loop {
            match chars.nth_back(0) {
                Some(char) => {
                    if let Some(digit) = char.to_digit(10) {
                        break digit.try_into().unwrap();
                    } // else: char is not a digit
                }
                None => panic!("Line has no digit?"),
            }
        }
    };

    (first, last)
}

pub fn main() {
    let input_lines: Vec<String> = read_input("input");
    let digits: Vec<(usize, usize)> = input_lines.iter().map(get_digits).collect();

    let solution: usize = digits.iter().fold(0, |accumulator, (dig1, dig2)| {
        let calibration_factor: usize = format!("{dig1}{dig2}").parse().unwrap();
        accumulator + calibration_factor
    });
    println!("Part 1: {}", solution);
}
