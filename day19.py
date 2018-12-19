from itertools import combinations
import sys

# Define opcodes -- from Day 16, only those needed for this problem
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

def setr(A, B, C, registers):
  registers[C] = registers[A]
opcodes["setr"] = setr

def seti(A, B, C, registers):
  registers[C] = A
opcodes["seti"] = seti

def gtrr(A, B, C, registers):
  registers[C] = 1 if registers[A] > registers[B] else 0
opcodes["gtrr"] = gtrr

def eqrr(A, B, C, registers):
  registers[C] = 1 if registers[A] == registers[B] else 0
opcodes["eqrr"] = eqrr

def run_program(ip_reg, registers, program, verbose=False):

    if verbose: print("A: %i  B: %i  C: %i  D: %i  E: %i  F: %i\n" % (tuple(registers)))

    ip_val = 0
    max_inst = len(program) - 1

    while 0 <= ip_val <= max_inst:

        ip_val_start = ip_val
        registers[ip_reg] = ip_val
        registers_start = registers[:]
        opcode, A, B, C = program[ip_val]
        opcodes[opcode](A, B, C, registers)
        ip_val = registers[ip_reg]
        ip_val += 1

        if verbose:
          print("(%s)" % ip_val_start, opcode, A, B, C)
          print("A: %i  B: %i  C: %i  D: %i  E: %i  F: %i" % (tuple(registers)))
          input()

        # print("ip=%i %s %s %i %i %i %s" % (ip_val_start, registers_start, opcode, A, B, C, registers))

    return registers

# =======================================

# Read in register for instruction pointer and program from file
program = []
with open(sys.argv[1]) as f:
    for line in f:
        if "#ip" in line:
            ip_reg = int(line.split()[1])
        else:
            inst, A, B, C = line.strip().split()
            program.append((inst, int(A), int(B), int(C)))

# Parts 1 and 2

# We first started by tracing out the execution of the program to figure
# out what it does. Verbosely running each instruction helps a lot:
# registers = run_program(ip_reg, [0, 0, 0, 0, 0, 0], program, True)

# After analyzing the program execution, we learn that it is executing the
# following code:

# [Calling the registers A, B, C, D, E, F]
# If register A is initially 0, set F to 931 (part 11)
# If it's 1, set F to 10551331 (part 2)
# A = 0
# for B in (1..F):
#   for E in (1..F):
#     if E * B == F:   # i.e. B and E divide F
#       A += B

# The number of iterations is equal to F**2, so executing the code to
# completion is feasible for part 1 (where F = 931) but not so for part 2
# (where F = 10551331).

# However, one can see that the final result (stored in register A)
# will be the sum of all divisors of F. One can directly find all divisors
# by repeated trial division (remembering not to go higher than sqrt(F)),
# or alternatively first find the prime factors of F and obtain the divisors
# from those.

# For instance, for part 1 where F = 931 the prime factors are [7, 7, 19].
# From those we can form the following divisors: [7, 19, 49, 133].
# And of course, 1 and F itself are also trivial divisors.
# So the answer is the sum of [1, 7, 19, 49, 133, 931].

# The following code computes the answer, given N
def solve(N):

  print("\nN=", N)

  # Obtain the (non-trivial) prime factors of N
  n = N
  prime_factors = []
  i = 2
  while i * i <= n:
    if n % i == 0:
      prime_factors.append(i)
      n //= i
    else:
      i += 1
  if n > 1:
    prime_factors.append(n)
  prime_factors.sort()
  print("prime factors:", prime_factors)

  # We now generate all divisors of N from the prime factors

  # Both 1 and N itself are (trivial) divisors
  divisors = set([1, N])

  # We now obtain all non-trivial divisors by considering all k-factor
  # combinations with 1 <= k < len(factors) and computing their product.
  # We must be careful not to add the same divisor twice (which can happen
  # when one of the prime factors appears multiple times).
  for k in range(1, len(prime_factors)):
    for comb in combinations(prime_factors, k):
      prod = 1
      for i in comb:
        prod *= i
      divisors.add(prod)

  divisors = sorted(list(divisors))
  print("all divisors:", divisors)

  # The answer is just the sum of all divisors
  return sum(divisors)

# The more direct solution finds the divisors by trial division of all
# integers up to sqrt(N). This can be much slower than the above if N
# is large.
def solve2(N):

  divisors = []

  i = 1
  while i * i <= N:
    if N % i == 0:
      divisors.append(i)
      if i*i != N:
        divisors.append(N // i)
    i += 1

  print("all divisors:", sorted(divisors))
  return sum(divisors)

print("Part 1:", solve(931))
print("Part 2:", solve(10551331))
