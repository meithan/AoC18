from string import ascii_lowercase

# Read in units
units = open("day5.in").read().strip()

# Reduced a sequence of units
# Exploits the fact that lower- and upper-case letters in ASCII are
# separated by 32 positions, and that appending or removing an item
# to/from the end of a list in Python is O(1) (amortized)
def reduce(units):
  new_units = []
  for i in range(len(units)):
    if len(new_units) > 0 and abs(ord(units[i])-ord(new_units[-1])) == 32:
      new_units.pop()
    else:
      new_units.append(units[i])
  return new_units

# Part 1

reduced = reduce(units)
print("Part 1:", len(reduced))

# Part 2

min_len = None
best_letter = None
for letter in ascii_lowercase:

  letter_up = letter.upper()
  units1 = [l for l in units if l != letter and l != letter_up]

  reduced = reduce(units1)

  if min_len is None or len(reduced) < min_len:
    min_len = len(reduced)
    best_letter = letter

print("Part 2:", min_len)
