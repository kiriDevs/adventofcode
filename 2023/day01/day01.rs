use std::fs;
use std::convert::TryInto;
use std::str::Chars;
use std::iter::Rev;

enum CharIter<'a> {
    Forward(Chars<'a>),
    Backward(Rev<Chars<'a>>)
}

impl<'a> Iterator for CharIter<'a> {
    type Item = char;
    fn next(&mut self) -> Option<Self::Item> {
        match self {
            CharIter::Forward(itr) => itr.next(),
            CharIter::Backward(itr) => itr.next(),
        }
    }
}

const TEXT_DIGITS: [(&str, u8); 10] = [
    ("zero", 0), ("one", 1), ("two", 2), ("three", 3), ("four", 4),
    ("five", 5), ("six", 6), ("seven", 7), ("eight", 8), ("nine", 9)
];

fn read_input(filename: &str) -> Vec<String> {
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

fn get_text_digit(text: &str) -> Option<u8> {
    for text_digit in TEXT_DIGITS {
        if text.ends_with(text_digit.0) || text.starts_with(text_digit.0) {
            return Some(text_digit.1);
        }
    }
    None
}

fn _get_first_digit(chars: CharIter, convert_text: bool, reversed: bool) -> u8 {
    let mut charbuf: String = String::new();

    for char in chars {
        if let Some(digit) = char.to_digit(10) {
            return digit.try_into().unwrap();
        }

        if reversed { charbuf.insert(0, char); }
        else { charbuf.push(char); }
        if convert_text {
            if let Some(text_digit) = get_text_digit(&charbuf) {
                return text_digit;
            }
        }
    }
    panic!("Line does not have a digit!");
}

fn get_first_digit(line: &str, convert_text: bool) -> u8 {
    _get_first_digit(CharIter::Forward(line.chars()), convert_text, false)
}

fn get_last_digit(line: &str, convert_text: bool) -> u8 {
    _get_first_digit(CharIter::Backward(line.chars().rev()).into_iter(), convert_text, true)
}

fn get_digits(line: &str, convert_text: bool) -> (u8, u8) {
    (get_first_digit(line, convert_text), get_last_digit(line, convert_text))
}

fn get_calibration_value((digit1, digit2): (u8, u8)) -> u8 {
    format!("{digit1}{digit2}").parse().unwrap()
}

fn find_solution(lines: Vec<String>, convert_text: bool) -> usize {
    lines.iter()
        .map(|line| get_digits(line, convert_text))
        .map(get_calibration_value)
        .fold(0, |acc, calibration_value| {
            acc + usize::from(calibration_value)
        })
}

pub fn main() {
    let input_lines: Vec<String> = read_input("input");
    println!("Part 1: {}", find_solution(input_lines.clone(), false));
    println!("Part 2: {}", find_solution(input_lines, true));
}
