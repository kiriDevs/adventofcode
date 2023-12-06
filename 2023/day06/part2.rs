use std::fs::read_to_string;

pub fn main() -> Result<(), std::io::Error> {
    let input = read_to_string("input")?;
    let mut input_lines = input.split("\n");
    let timestr = input_lines.next().unwrap();
    let diststr = input_lines.next().unwrap();

    timestr.trim().chars().

    println!("time={} dist={}", timestr, diststr);

    Ok(())
}
