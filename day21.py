from queue import Queue
import sys

# The elfcode instruction set
def addr(A, B, C, regs): regs[C] = regs[A] + regs[B]
def addi(A, B, C, regs): regs[C] = regs[A] + B
def mulr(A, B, C, regs): regs[C] = regs[A] * regs[B]
def muli(A, B, C, regs): regs[C] = regs[A] * B
def banr(A, B, C, regs): regs[C] = regs[A] & regs[B]
def bani(A, B, C, regs): regs[C] = regs[A] & B
def borr(A, B, C, regs): regs[C] = regs[A] | regs[B]
def bori(A, B, C, regs): regs[C] = regs[A] | B
def setr(A, B, C, regs): regs[C] = regs[A]
def seti(A, B, C, regs): regs[C] = A
def gtir(A, B, C, regs): regs[C] = 1 if A > regs[B] else 0
def gtri(A, B, C, regs): regs[C] = 1 if regs[A] > B else 0
def gtrr(A, B, C, regs): regs[C] = 1 if regs[A] > regs[B] else 0
def eqir(A, B, C, regs): regs[C] = 1 if A == regs[B] else 0
def eqri(A, B, C, regs): regs[C] = 1 if regs[A] == B else 0
def eqrr(A, B, C, regs): regs[C] = 1 if regs[A] == regs[B] else 0

# Runs the program using register ip_reg as instruction pointer
# and start_registers as the initial register values
# Returns the values of the registers at end of execution
def run_program(ip_reg, program, start_registers, verbose=False):

    registers = start_registers[:]

    if verbose: print("A: %i  B: %i  C: %i  D: %i  E: %i  F: %i\n" % (tuple(registers)))

    ip_val = 0
    while True:

        cur_inst = ip_val
        if cur_inst > len(program) - 1: break
        registers[ip_reg] = cur_inst
        opcode, A, B, C = program[cur_inst]
        eval(opcode)(A, B, C, registers)
        ip_val = registers[ip_reg] + 1

        if verbose:
          print("(%s)" % cur_inst, opcode, A, B, C)
          print("A: %i  B: %i  C: %i  D: %i  E: %i  F: %i" % (tuple(registers)))
          input()

    return registers

# ===========================

from math import floor

# Read in register for instruction pointer and program from file
program = []
with open(sys.argv[1]) as f:
    for line in f:
        if "#ip" in line:
            ip_reg = int(line.split()[1])
        else:
            inst, A, B, C = line.strip().split()
            program.append((inst, int(A), int(B), int(C)))

# Tracing program execution helps translate it into Python code
# registers = [0, 0, 0, 0, 0, 0]
# run_program(ip_reg, program, registers, verbose=True)
# sys.exit()

# After analyzing the elfcode, we can reduce it to the following Python code:

# F = 2**16
# C = 16123384
# while True:
#
#   while True:
#     C = (((C+(F%256))%2**24)*65899)%2**24
#     if F < 256: break
#     else: F = int(floor(F/256))
#
#   if C == A:
#     # Program stops
#     break
#   else:
#     F = C | 65536
#     C = 16123384

# The program essentially computes a sequence of values of C by repeatedly
# applying that transformation. One of two things will happen:
# 1) C == A at some point before a value of C is repeated, in which
#    case the program stops at that C value;
# 2) A value of C is repeated before C == A. Since the program is
#    deterministic, future execution will simply loop through a finite cycle
#    of values of C from that point on, thus never stopping.
# Thus, to find the answers, we compute the sequence of values of C until
# a repetition is found. Setting A = 0 this happens after 10264 iterations.

# For Part 1, the answer is the first value of C that is compared against A,
# so we keep track of it.

# The answer to Part 2 is the latest value of C to be seen for the first
# time fore the cycle begins.

part1_ans = None
Cs = []
seen = set()

F = 2**16
C = 16123384
while True:

  while True:
    C = (((C+(F%256))%2**24)*65899)%2**24
    if F < 256:
      break
    else:
      F = int(floor(F/256))

  Cs.append(C)
  if C in seen:
    break
  else:
    seen.add(C)

  if part1_ans is None:
    part1_ans = C

  if C == A:
    # Program stops
    break
  else:
    F = C | 65536
    C = 16123384

print("Repeated after %i iterations" % len(Cs))

part2_ans = None
seen = set()
for i in range(len(Cs)):
  if Cs[i] not in seen:
    part2_ans = Cs[i]
  seen.add(Cs[i])

print("Part 1:", part1_ans)
print("Part 2:", part2_ans)
