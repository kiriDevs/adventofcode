use std::fs;
use std::cmp::min;

struct Gift { length: u64, width: u64, height: u64 }
impl Gift {
    /// Create a Gift object from a String
    fn from_string(string: &String) -> Self {
        let mut factors = string.trim().split("x").map(|num| {
            num.parse::<u64>().unwrap()
        });
        let (length, width, height) = (
            factors.next().unwrap(),
            factors.next().unwrap(),
            factors.next().unwrap()
        );
        if factors.next().is_some() {
            panic!("Invalid gift specification");
        }
        Self { length, width, height }
    }

    /// The full surface area of the gift
    fn area(&self) -> u64 {
        (2 * self.length * self.width)
        + (2 * self.width * self.height)
        + (2 * self.length * self.height)
    }

    /// The overhead of packing paper used when packing the gift
    fn packing_overhead(&self) -> u64 {
        min(
            min(self.length * self.width, self.width * self.height),
            self.length * self.height
        )
    }

    /// The volume of the box (for ribbon bows)
    fn volume(&self) -> u64 {
        self.length * self.width * self.height
    }

    /// Perimeter of the smallest side
    fn perimeter(&self) -> u64 {
        min(
            min(
                (2 * self.length) + (2 * self.width),
                (2 * self.width) + (2 * self.height)
            ),
            (2 * self.length) + (2 * self.height)
        )
    }
}

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

pub fn main() {
    let gifts = read_input("day02.in").iter()
        .map(Gift::from_string).collect::<Vec<Gift>>();

    let solution1 = gifts.iter()
        .map(|gift| gift.area() + gift.packing_overhead())
        .fold(0, |accumulator, packing_paper| accumulator + packing_paper);
    let solution2 = gifts.iter()
        .map(|gift| gift.perimeter() + gift.volume())
        .fold(0, |accumulator, ribbon| accumulator + ribbon);

    println!("Part 1: {}\nPart 2: {}", solution1, solution2);
}
