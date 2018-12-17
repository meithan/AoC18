import sys

# Define opcodes
opcodes = {}

def addr(A, B, C, registers):
  registers[C] = registers[A] + registers[B]
opcodes["addr"] = addr

def addi(A, B, C, registers):
  registers[C] = registers[A] + B
opcodes["addi"] = addi

def mulr(A, B, C, registers):
  registers[C] = registers[A] * registers[B]
opcodes["mulr"] = mulr

def muli(A, B, C, registers):
  registers[C] = registers[A] * B
opcodes["muli"] = muli

def banr(A, B, C, registers):
  registers[C] = registers[A] & registers[B]
opcodes["banr"] = banr

def bani(A, B, C, registers):
  registers[C] = registers[A] & B
opcodes["bani"] = bani

def borr(A, B, C, registers):
  registers[C] = registers[A] | registers[B]
opcodes["borr"] = borr

def bori(A, B, C, registers):
  registers[C] = registers[A] | B
opcodes["bori"] = bori

def setr(A, B, C, registers):
  registers[C] = registers[A]
opcodes["setr"] = setr

def seti(A, B, C, registers):
  registers[C] = A
opcodes["seti"] = seti

def gtir(A, B, C, registers):
  registers[C] = 1 if A > registers[B] else 0
opcodes["gtir"] = gtir

def gtri(A, B, C, registers):
  registers[C] = 1 if registers[A] > B else 0
opcodes["gtri"] = gtri

def gtrr(A, B, C, registers):
  registers[C] = 1 if registers[A] > registers[B] else 0
opcodes["gtrr"] = gtrr

def eqir(A, B, C, registers):
  registers[C] = 1 if A == registers[B] else 0
opcodes["eqir"] = eqir

def eqri(A, B, C, registers):
  registers[C] = 1 if registers[A] == B else 0
opcodes["eqri"] = eqri

def eqrr(A, B, C, registers):
  registers[C] = 1 if registers[A] == registers[B] else 0
opcodes["eqrr"] = eqrr

opcode_names = sorted(opcodes.keys())

# Represents a sample execution
class Sample:
  def __init__(self, before, inst, after):
    self.before = before
    self.code = inst[0]
    self.args = inst[1:]
    self.after = after
  def __repr__(self):
    return "%s -> %s%s -> %s" % (self.before, self.code, self.args, self.after)

# Executes opcode with arguments on given registers
# Note that this modifies the passed registers
def exec_opcode(opcode_name, registers, arguments):
  A = arguments[0]
  B = arguments[1]
  C = arguments[2]
  opcodes[opcode_name](A, B, C, registers)

# Tries running an opcode_name on the given sample, and returns
# whether the result matches that contained in the sample
def check_sample(opcode_name, sample):
  registers = sample.before[:]
  exec_opcode(opcode_name, registers, sample.args)
  result = tuple(registers)
  return result == sample.after

# Verifies that code and name match for all the given samples
def verify_code(opcode_name, opcode_code, samples):
  for sample in samples:
    if sample.code == opcode_code:
      match = check_sample(opcode_name, sample)
      if not match:
        return False
  return True

# =======================================

# Read in samples and program
samples = []
program = []
with open(sys.argv[1]) as f:
  blank_lines = 0
  while True:
    line = f.readline()
    if line == "": break
    line = line.strip()
    if len(line) == 0:
      blank_lines += 1
    elif "Before" in line:
      blank_lines = 0
      before = [int(x) for x in eval(line.split(": ")[1])]
      line = f.readline().strip()
      inst = tuple(int(x) for x in line.split())
      line = f.readline().strip()
      after = tuple(int(x) for x in eval(line.split(": ")[1]))
      samples.append(Sample(before, inst, after))
    if blank_lines == 3:
      while True:
        line = f.readline().strip()
        if line == "":
          break
        inst = tuple(int(x) for x in line.split())
        program.append(inst)
      break

# Part 1

# Just check every opcode for every sample and record matches
samples_3_more = 0
for sample in samples:
  matches = 0
  for opcode_name in opcodes.keys():
    match = check_sample(opcode_name, sample)
    if match:
      matches += 1
  if matches >= 3:
    samples_3_more += 1

print("Part 1:", samples_3_more)

# Part 2

# Stores list of possible opcode names for each opcode numeric value
possible = []
for i in range(16):
  s = set()
  for name in opcode_names:
    s.add(name)
  possible.append(s)

# Check all samples and take out possibilities that fail
for sample in samples:
  for name in opcode_names:
    match = check_sample(name, sample)
    if not match:
      if name in possible[sample.code]:
        possible[sample.code].remove(name)

# Assign found for single options
found_codes = {}

# Repeat the following until all opcode values are found
# This was meant to be a pre-processing round before attempting
# to solve a CSP, but that wasn't needed as all codes were found
while len(found_codes) < 16:

  # Look for codes having a single possibility
  for code in range(16):
    if len(possible[code]) == 1:
      name = next(iter(possible[code]))
      found_codes[code] = name

  # Remove found codes from other possibilities
  for found_code in found_codes:
    found_name = found_codes[found_code]
    for other_code in range(16):
      if found_code != other_code:
        if found_name in possible[other_code]:
          possible[other_code].remove(found_name)

# Execute program
registers = [0, 0, 0, 0]
for instruction in program:
  code = instruction[0]
  args = instruction[1:]
  exec_opcode(found_codes[code], registers, args)

print("Final:", registers)
print("Part 2:", registers[0])
