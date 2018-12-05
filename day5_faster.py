from string import ascii_lowercase

# Read in units
with open("day5.in") as f:
  for line in f:
    units = line.strip()
#units = "YDdATiIQqtKkNnqmMQqHUuoOoOxXhHhMXRrxAXxdDYyamrnAaVPpPVv"

def reduce(units):
  while True:
    new_units = ""
    done = True
    i = 0
    while i < len(units):
      if i == len(units) - 1:
        new_units += units[i]
        break
      if units[i].lower() == units[i+1].lower() and (units[i].islower() and units[i+1].isupper() or units[i].isupper() and units[i+1].islower()):
        done = False
        i += 2
      else:
        new_units += units[i]
        i += 1
    if done:
      return units
    else:
      units = new_units

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
