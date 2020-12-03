from string import ascii_lowercase

# Read in units
units = open("day5.in").read().strip()

# Returns a reduced sequence of units after reactions
# Exploits the fact that lower- and upper-case letters in ASCII are
# separated by 32 positions, and that appending or removing an item
# to/from the end of a list in Python is (amortized) O(1).
def reduce(units):
  new_units = []
  for c in [ord(x) for x in units]:
    if len(new_units) > 0 and abs(c - new_units[-1]) == 32:
      new_units.pop()
    else:
      new_units.append(c)
  return new_units

# Part 1

reduced_units = "".join([chr(x) for x in reduce(units)])
print("Part 1:", len(reduced_units))

# Part 2

# A big optimization is realzing the result of Part 1 (the shorter
# reduced list of units) can be used as the starting point for Part 2
min_len = None
for letter in ascii_lowercase:

  # String replace is fast
  units1 = reduced_units.replace(letter, "").replace(letter.upper(), "")
  reduced = reduce(units1)

  if min_len is None or len(reduced) < min_len:
    min_len = len(reduced)

print("Part 2:", min_len)
