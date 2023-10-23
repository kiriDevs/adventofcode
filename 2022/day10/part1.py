from tqdm import tqdm

RECORD_SIGNAL_STRENGTHS: [int] = [20, 60, 100, 140, 180, 220]


class Processor:
    program: [str]
    clock: int
    reg_x: int

    runtime_stack: [int]

    def __init__(self, program: [str]):
        self.program = program
        self.clock = 0
        self.reg_x = 1

        self.runtime_stack = []

    def clock_tick(self):
        if (self.clock % 40) in [self.reg_x - 1, self.reg_x, self.reg_x + 1]:
            print("#", end="")
        else:
            print(".", end="")
        self.clock += 1
        if (self.clock % 40) == 0:
            print("\n", end="")
        if self.clock in RECORD_SIGNAL_STRENGTHS:
            signal_strength: int = self.clock * self.reg_x
            self.runtime_stack.append(signal_strength)

    def noop(self):
        self.clock_tick()

    def add_x(self, amount: int):
        self.clock_tick()
        self.clock_tick()
        self.reg_x += amount

    def run_instruction(self, instruction):
        instruction_parts: [str] = instruction.split(" ")
        if instruction_parts[0] == "noop":
            self.noop()
        else:
            self.add_x(int(instruction_parts[1]))

    def run(self) -> [int]:
        self.reg_x = 1
        self.runtime_stack = []
        for instruction in self.program:
            self.run_instruction(instruction)


def main():
    with open("input", "r", encoding="utf-8") as input_file:
        input_lines: [str] = [a.strip() for a in input_file.read().strip().split("\n")]
    processor: Processor = Processor(input_lines)
    processor.run()
    print(f"Part 1: {sum(processor.runtime_stack)}")


if __name__ == "__main__":
    main()
