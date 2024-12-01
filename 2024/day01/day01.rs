use std::fs;
use std::collections::HashMap;
use std::hash::Hash;

struct Lists {
    left: Vec<u32>,
    right: Vec<u32>,
}

impl Lists {
    fn new(mut left: Vec<u32>, mut right: Vec<u32>) -> Self {
        left.sort(); right.sort();

        let len = left.len();
        if right.len() != len { panic!("Lists differ in length?") }
        Self { left, right }
    }

    fn nth_left(&self, inx: usize) -> &u32 {
        self.left.get(inx).expect("Out of bounds read (l)")
    }
    fn nth_right(&self, inx: usize) -> &u32 {
        self.right.get(inx).expect("Out of bounds read (r)")
    }

    fn left(&self) -> &Vec<u32> { &self.left }
    fn right(&self) -> &Vec<u32> { &self.right }
    fn len(&self) -> usize { self.left.len() }
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

fn parse_lists(input_lines: Vec<String>) -> Lists {
    let mut left: Vec<u32> = Vec::new();
    let mut right: Vec<u32> = Vec::new();

    for input_line in input_lines { 
        let mut nums = input_line.split("   ");
        left.push(nums.next().expect("Missing left number").parse().expect("Invalid left number"));
        right.push(nums.next().expect("Missing right number").parse().expect("Invalid right number"));
    }

    Lists::new(left, right)
}

fn part1(lists: &Lists) -> u64 {
    let mut diff_score: u64 = 0;
    for inx in 0..lists.len() {
        let left: i32 = *lists.nth_left(inx) as i32;
        let right: i32 = *lists.nth_right(inx) as i32;
        let diff = (left - right).abs();
        diff_score += diff as u64;
    }
    diff_score
}

fn get_or_default<'a, K, V>(
    map: &'a HashMap<K, V>,
    key: &K,
    default_value: &'static V
) -> &'a V where K: Eq+Hash {
    return match map.get(key) {
        Some(value) => value,
        None => default_value
    }
}

fn part2(lists: &Lists) -> u64 {
    let mut similar_score: u64 = 0;
    let mut count_map: HashMap<u32, usize> = HashMap::new();
    for right_num in lists.right() {
        count_map.insert(*right_num, get_or_default(&count_map, right_num, &0) + 1);
    }
    for left_num in lists.left() {
        similar_score += (*left_num as u64) * (*get_or_default(&count_map, left_num, &0) as u64);
    }
    similar_score
}

pub fn main() {
    let input_text = read_input("input");
    let lists: Lists = parse_lists(input_text);

    let solution1 = part1(&lists);
    let solution2 = part2(&lists);
    println!("Part 1: {}\nPart 2: {}", solution1, solution2);
}
