from tqdm import tqdm
from wtslog import Logger

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

LOGGER: Logger = Logger(OUTPUT_PATH)

with open(INPUT_PATH, "r") as input_file:
    input_lines: [str] = input_file.read().strip().split("\n")
input_lines = [line.strip() for line in input_lines]


class Coordinate:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    @classmethod
    def from_str(cls, from_str: str) -> 'Coordinate':
        x, y = from_str.split(",")
        x = int(x)
        y = int(y)
        return cls(x, y)

    def __str__(self) -> str:
        return f"({self.x:3} | {self.y:3})"

    def __repr__(self) -> str:
        return self.__str__()


class Field:
    location: Coordinate
    vent_value: int

    def __init__(self, coordinate: Coordinate):
        self.coordinate = coordinate
        self.vent_value = 0

    def __str__(self) -> str:
        return f"[Field at {self.coordinate} - {self.vent_value}]"

class VentLine:
    start: Coordinate
    end: Coordinate
    all_coords: [Coordinate]

    @staticmethod
    def would_be_straight(start: Coordinate, end: Coordinate):
        return (start.x == end.x) or (start.y == end.y)

    def __init__(self, start: Coordinate, end: Coordinate):
        self.start = start
        self.end = end

        self.all_coords = []
        if start.x == end.x and start.y < end.y:
            y_offsets = range((end.y - start.y) + 1)
            for y_offset in y_offsets:
                y = start.y + y_offset
                coord: Coordinate = Coordinate(start.x, y)
                self.all_coords.append(coord)
        elif start.x == end.x and start.y > end.y:
            y_offsets = range((start.y - end.y) + 1)
            for y_offset in y_offsets:
                y = end.y + y_offset
                coord: Coordinate = Coordinate(start.x, y)
                self.all_coords.append(coord)
        elif start.y == end.y and start.x < end.x:
            x_offsets = range((end.x - start.x) + 1)
            for x_offset in x_offsets:
                x = start.x + x_offset
                coord: Coordinate = Coordinate(x, start.y)
                self.all_coords.append(coord)
        elif start.y == end.y and start.x > end.x:
            x_offsets = range((start.x - end.x) + 1)
            for x_offset in x_offsets:
                x = end.x + x_offset
                coord: Coordinate = Coordinate(x, start.y)
                self.all_coords.append(coord)
        # else:
            # Not implemented because it doesn't matter for part1
        LOGGER.log(self.all_coords.__str__())

    def __str__(self) -> str:
        return f"[VentLine {self.start} -> {self.end} (len {len(self)})]"

    def __len__(self) -> int:
        return len(self.all_coords)


class Grid:
    fields: [[Field]]

    def __init__(self, width: int, height: int):
        self.fields = []
        for line_inx in range(height):
            line: [Field] = []
            for col_inx in range(width):
                field: Field = Field(Coordinate(col_inx, line_inx))
                line.append(field)
            self.fields.append(line)

    def add_vents(self, from_line: VentLine):
        LOGGER.log(f"Adding {from_line} to board...")
        LOGGER.indent()
        for coord in from_line.all_coords:
            self.fields[coord.y][coord.x].vent_value += 1
        LOGGER.unindent()
        LOGGER.log(f"Successfully added {len(from_line)} vents to the board.")

    def count_ventline_intersections(self) -> int:
        intersection_count: int = 0
        for grid_line_inx in tqdm(range(len(self.fields))):
            grid_line: [Field] = self.fields[grid_line_inx]
            LOGGER.log(f"Counting intersects in line {grid_line_inx}...")
            LOGGER.indent()
            intersects_on_line: int = 0
            for grid_field in grid_line:
                if grid_field.vent_value > 1:
                    intersects_on_line += 1
                    LOGGER.log(f"Field {grid_field} is an intersection.")
            LOGGER.unindent()
            LOGGER.log(f"Found {intersects_on_line} intersections.")
            intersection_count += intersects_on_line
        return intersection_count


LOGGER.tee("Creating vent line objects...")
LOGGER.indent()
vent_lines: [VentLine] = []
for input_line in tqdm(input_lines):
    LOGGER.log(f"Creating vent line {input_line}")
    LOGGER.indent()

    start, end = input_line.split(" -> ")
    start = Coordinate.from_str(start)
    end = Coordinate.from_str(end)

    line = VentLine(start, end)
    vent_lines.append(line)

    LOGGER.unindent()
    LOGGER.log(line.__str__())
LOGGER.unindent()
LOGGER.tee(f"Created {len(vent_lines)} vent line objects.")

LOGGER.tee()

LOGGER.tee("Detecting field dimensions...")
LOGGER.indent()
highest_x: int = 0
highest_y: int = 0
for line in tqdm(vent_lines):
    highest_x = max(line.start.x, line.end.x, highest_x)
    highest_y = max(line.start.y, line.end.y, highest_y)
# The +1 converts from highest index (0-based) to dimensions (1-based)
g_width: int = highest_x + 1
g_height: int = highest_y + 1
LOGGER.log(f"Highest values: x:{highest_x}, y:{highest_y}")
# Maybe my input was just square by chance?
if not g_width == g_height:
    g_width = max(g_width, g_height)
    g_height = max(g_width, g_height)
    LOGGER.tee(f"Adjusted both values to highest ({g_width}) to get a square.")
LOGGER.unindent()
LOGGER.tee(f"Detected dimensions {g_width}x{g_height}.")
LOGGER.tee("Creating grid...")
grid: Grid = Grid(g_width, g_height)

LOGGER.tee()

LOGGER.tee("Committing vent lines to grid...")
LOGGER.indent()
for vent_line in tqdm(vent_lines):
    grid.add_vents(vent_line)
LOGGER.unindent()
LOGGER.tee("Done.")

LOGGER.tee()

LOGGER.tee("Counting vent line intersections...")
LOGGER.indent()
SOLUTION: int = grid.count_ventline_intersections()
LOGGER.unindent()
LOGGER.tee(f"SOLUTION: There are {SOLUTION} intersections.")

# Write our logs to the output file
LOGGER.dump_log()
