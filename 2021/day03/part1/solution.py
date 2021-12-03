from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Loading input...")
with open(INPUT_PATH, "r") as input_file:
    input_lines: [str] = input_file.read().strip().split("\n")
input_lines = [line.strip() for line in tqdm(input_lines)]
LOGGER.tee(f"Successfully loaded {len(input_lines)} lines of input.")
LOGGER.tee()

LOGGER.tee("Processing input")
LOGGER.indent()
counts: [int] = [0 for _ in input_lines[0]]
for indx in tqdm(range(len(input_lines))):
    input_line: str = input_lines[indx]
    bits: [str] = list(input_line)
    LOGGER.log(f"{indx:04} - {bits}")
    LOGGER.indent()
    for bit_indx in range(len(bits)):
        bit: str = bits[bit_indx]
        if bit == "1":
            counts[bit_indx] += 1
            LOGGER.log(
                f"{bit_indx:2} = {bit}"
                + f" | {counts[bit_indx]-1:03} -> {counts[bit_indx]:03}"
            )
        else:
            LOGGER.log(f"{bit_indx:2} = {bit}")
            
    LOGGER.unindent()
LOGGER.unindent()
LOGGER.tee()
LOGGER.tee([f"{indx:02}:{counts[indx]:03}" for indx in range(len(counts))])
LOGGER.tee()

LOGGER.tee("Assembling final numbers")
gamma: [str] = ["0" for _ in range(len(input_lines[0]))]
epsilon: [str] = gamma.copy()
for bit_indx in range(len(counts)):
    bit_count: int = counts[bit_indx]
    #!! Might have to change this to '>=' if it doesn't work, I don't know
    #!! which one takes precendence if it's a tie. However, in part2, 1 takes
    #!! preference, so it might actually make sense to use that. But I was fine
    #!! with this and haven't heard anything else yet, so I'll keep it like
    #!! this for now
    if bit_count > len(input_lines)/2:
        gamma[bit_indx] = "1"
    else:
        epsilon[bit_indx] = "1"

gamma_str: str = "".join(gamma)
epsilon_str: str = "".join(epsilon)
gamm: int = int(gamma_str, 2)
epsi: int = int(epsilon_str, 2)
result: int = gamm * epsi

LOGGER.tee(f"Gamma : {gamm}")
LOGGER.tee(f"Epsilon: {epsi}")
LOGGER.tee()
LOGGER.tee(f"Result: {result}")

# Write our logs to the output file
LOGGER.dump_log()
