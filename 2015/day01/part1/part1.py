INPUT_PATH = "../day01.in"
OUTPUT_PATH = "./part1.out"

with open("../../_common/logger.py", "r") as logger_module:
    exec(logger_module.read())
LOGGER = Logger(OUTPUT_PATH)

DOWN = ")"

with open("../day01.in", "r") as input_file:
  INPUT_TEXT = input_file.read()
  INPUT_TEXT = INPUT_TEXT.strip()

step_count: int = 0


# Start by removing () and )( recursively (because they cancel out)
def removeCanceling(fromString: str) -> str:
  global LOGGER
  global step_count

  step_id = step_count
  step_count += 1

  LOGGER.log(f"Starting step {step_id}> {fromString}")

  res: str
  if "()" in fromString or ")(" in fromString:
    res = fromString.replace("()", "")
    res = res.replace(")(", "")
    res = removeCanceling(res)
  else:
    res = fromString

  return res



LOGGER.indent()
resultText: str = removeCanceling(INPUT_TEXT)
LOGGER.unindent()
LOGGER.tee("Done.")

LOGGER.tee()

LOGGER.log("Result:")
LOGGER.log(resultText)
LOGGER.log()

LOGGER.tee("Counting rest...")
LOGGER.indent()

floornumber = len(resultText)
if resultText[0] == DOWN:
  LOGGER.log(f"Flipping floornumber because the character is DOWN ['{DOWN}']")
  floornumber *= -1;
else:
  LOGGER.log(f"Rest char is not DOWN ['{DOWN}'] - not flipping floornumber")

LOGGER.unindent()
LOGGER.tee(f"Santa has to go to floor {floornumber}!")

LOGGER.dmp()
exit(0)
