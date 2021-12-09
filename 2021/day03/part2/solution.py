from tqdm import tqdm

INPUT_PATH: str = "../input"
OUTPUT_PATH: str = "./output_py"

from wtslog import Logger
LOGGER: Logger = Logger(OUTPUT_PATH)

LOGGER.tee("Reading input")
with open(INPUT_PATH, "r") as infile:
    innums: [str] = [a.strip() for a in infile.read().strip().split("\n")]
LOGGER.tee(f"Successfully read {len(innums)} numbers")

LOGGER.tee()

oxystrs: [str] = innums.copy()
for binx in tqdm(range(len(oxystrs[0]))):
    LOGGER.log(f"Counting numbers for bit {binx:2}")
    LOGGER.indent()
    bcount: int = 0
    for sinx, oxystr in enumerate(oxystrs):
        if oxystr[binx] == "1":
            old: int = bcount
            LOGGER.log(f"{sinx:4} has a 1 at {binx:2}: {old:3} --> {bcount:3}")
            bcount += 1
    LOGGER.unindent()
    LOGGER.log(f"Bit {binx:2} was set {bcount} times.")
    del_ones: bool = bcount < (len(oxystrs) / 2)

    LOGGER.log(f"Marking 1s for deletion: {del_ones}")
    LOGGER.indent()
    deletions: [int] = []
    for sinx, oxystr in enumerate(oxystrs):
        if (
                (oxystr[binx] == "1" and del_ones)
                or (oxystr[binx] == "0" and not del_ones)
            ):
            LOGGER.log(f"Marking {sinx:4} for deletion")
            deletions.append(sinx)
    LOGGER.unindent()
    LOGGER.log(f"Marked {len(deletions)} numbers for deletion.")

    LOGGER.log("Deleting marked numbers...")
    LOGGER.indent()
    deletions.sort()
    while len(deletions) > 0:
        delinx: int = deletions.pop()
        LOGGER.log(f"Deleting number {delinx:4}")
        del oxystrs[delinx]
    LOGGER.unindent()
    LOGGER.log(f"{len(oxystrs)} numbers remain.")
    LOGGER.log()
oxyratingstr: str = oxystrs[0]
oxyrate: int = int(oxyratingstr, 2)
LOGGER.tee(f"Your Oxygen-Rating is {oxyratingstr} ({oxyrate})")

coostrs: [str] = innums.copy()
for binx in tqdm(range(len(coostrs[0]))):
    if len(coostrs) == 1:
        continue
    LOGGER.log(f"Counting numbers for bit {binx:2}")
    LOGGER.indent()
    bcount: int = 0
    for sinx, coostr in enumerate(coostrs):
        if coostr[binx] == "1":
            old: int = bcount
            LOGGER.log(f"{sinx:4} has a 1 at {binx:2}: {old:3} --> {bcount:3}")
            bcount += 1
    LOGGER.unindent()
    LOGGER.log(f"Bit {binx:2} was set {bcount} times.")
    del_ones: bool = bcount >= (len(coostrs) / 2)

    LOGGER.log(f"Marking 1s for deletion: {del_ones}")
    LOGGER.indent()
    deletions: [int] = []
    for sinx, coostr in enumerate(coostrs):
        if (
                (coostr[binx] == "1" and del_ones)
                or (coostr[binx] == "0" and not del_ones)
            ):
            LOGGER.log(f"Marking {sinx:4} for deletion")
            deletions.append(sinx)
    LOGGER.unindent()
    LOGGER.log(f"Marked {len(deletions)} numbers for deletion.")

    LOGGER.log("Deleting marked numbers...")
    LOGGER.indent()
    deletions.sort()
    while len(deletions) > 0:
        delinx: int = deletions.pop()
        LOGGER.log(f"Deleting number {delinx:4}")
        del coostrs[delinx]
    LOGGER.unindent()
    LOGGER.log(f"{len(coostrs)} numbers remain.")
    LOGGER.log()
cooratingstr: str = coostrs[0]
coorate: int = int(cooratingstr, 2)
LOGGER.tee(f"Your CO2-Rating is {cooratingstr} ({coorate})")

LOGGER.tee()
LOGGER.tee(f"Your result is {oxyrate}*{coorate}={oxyrate*coorate}")

# Write our logs to the output file
LOGGER.dump_log()
