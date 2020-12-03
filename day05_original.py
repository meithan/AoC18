from string import ascii_lowercase

# Read in units
with open("day5.in") as f:
  for line in f:
    units = line.strip()

def reduce(units):
  while True:
    found = False
    for i in range(len(units)-1):
      if units[i].lower() == units[i+1].lower() and (units[i].islower() and units[i+1].isupper() or units[i].isupper() and units[i+1].islower()):
        found = True
        break
    if not found: break
    units = units[:i] + units[i+2:]
    #print(len(units))
  return units

# Part 1

reduced = reduce(units)
print("Part 1:", len(reduced))

# Part 2

print(len(units))
min_len = None
best_letter = None
for letter in ascii_lowercase:

  units1 = "".join([l for l in units if l != letter])
  units1 = "".join([l for l in units1 if l != letter.upper()])
  print(letter, len(units1))

  reduced = reduce(units1)
  if min_len is None or len(reduced) < min_len:
    min_len = len(reduced)
    best_letter = letter

  print(len(reduced))

print("Part 2:", min_len)
