from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Processing input...")
LOGGER.indent()

with open(INPUT_PATH, "r") as infile:
    inparagraphs: [str] = infile.read().strip().split("\n\n")
in_dot_strs: [str] = inparagraphs[0].split("\n")
in_fold_strs: [str] = inparagraphs[1].split("\n")

LOGGER.log("Reading point positions...")
LOGGER.indent()
dots: [(int, int)] = []
for dotstr in in_dot_strs:
    x, y = dotstr.split(",")
    dot: (int, int) = (int(x), int(y))
    dots.append(dot)
    LOGGER.log(dot)
LOGGER.unindent()
LOGGER.log(f"Read {len(dots)} point positions.")

LOGGER.log("Reading fold instructions...")
LOGGER.indent()
folds: [(str, int)] = []
for foldstr in in_fold_strs:
    foldstr = foldstr.replace("fold along ", "")
    axis, coord = foldstr.split("=")
    fold: (str, int) = (axis, int(coord))
    folds.append(fold)
    LOGGER.log(fold)
LOGGER.unindent()
LOGGER.log(f"Read {len(folds)} fold instructions.")

width: int = max([dot[0] for dot in dots]) + 1
height: int = max([dot[1] for dot in dots]) + 1
LOGGER.log(f"Detected dimensions: {width}x{height}")
LOGGER.unindent()
LOGGER.tee("Done.")

LOGGER.tee()

LOGGER.tee("Creating paper...")
LOGGER.indent()

PAPER: [[str]] = [["." for _ in range(width)] for _ in range(height)]
LOGGER.log("Starting population...")
LOGGER.indent()
for x, y in dots:
    PAPER[y][x] = "#"
LOGGER.unindent()

LOGGER.unindent()
LOGGER.tee("Created paper.")

LOGGER.tee()

LOGGER.tee("Folding the paper...")
LOGGER.indent()
for foldinx, fold in tqdm(enumerate(folds)):
    LOGGER.log(f"Starting fold {foldinx}")
    LOGGER.indent()
    width = max([dot[0] for dot in dots]) + 1
    height = max([dot[1] for dot in dots]) + 1
    foldaxis, foldcoord = fold
    if foldaxis == "x":
        stepcount: int = width - foldcoord - 1
        steprange = range(1, stepcount+1)
        for stepvalue in steprange:
            check_x = foldcoord + stepvalue
            set_x = foldcoord - stepvalue
            for y in range(height):
                try:
                    if PAPER[y][check_x] == "#":
                        PAPER[y][set_x] = "#"
                except IndexError: 
                    pass
        for stepvalue in steprange:
            x: int = width - stepvalue
            for y in range(height):
                try:
                    del PAPER[y][x]
                except IndexError:
                    pass
    elif foldaxis == "y":
        stepcount: int = height - foldcoord - 1
        steprange = range(1, stepcount+1)
        for stepvalue in steprange:
            check_y = foldcoord + stepvalue
            set_y = foldcoord - stepvalue
            for x in range(width):
                try:
                    if PAPER[check_y][x] == "#":
                        PAPER[set_y][x] = "#"
                except IndexError: 
                    pass
        for stepvalue in steprange:
            y: int = height - stepvalue
            try:
                del PAPER[y]
            except IndexError:
                pass
    else:
        raise Error(f"Invalid input in fold {foldinx}!")
    LOGGER.unindent()
LOGGER.unindent()
LOGGER.tee("Completed folding.")

LOGGER.tee()

LOGGER.tee("Counting dots...")
dotcount: int = sum([line.count("#") for line in PAPER])
LOGGER.tee(f"SOLVE: There are {dotcount} dots visible")

LOGGER.tee()
[LOGGER.tee(l) for l in PAPER]

# Write our logs to the output file
LOGGER.dump_log()
