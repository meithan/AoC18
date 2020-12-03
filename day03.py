import re

# Read in claims from input
claims = []
with open("day3.in") as f:
  # Regexes for simpler parsing!
  pattern = r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
  for line in f:
    match = re.match(pattern, line.strip())
    claims.append([int(x) for x in match.groups(1)])

# Part 1

# Initialize the grid of squares, empty
N = 1000
fabric = [[] for i in range(N)]
for i in range(N):
  for j in range(N):
    fabric[i].append([])

# For each claim, add its ID to the squares it covers
for ID, xpos, ypos, width, height in claims:
  for i in range(xpos, xpos+width):
    for j in range(ypos, ypos+height):
      fabric[i][j].append(ID)

# Count how many squares have two or more claims
count = 0
for i in range(N):
  for j in range(N):
    if len(fabric[i][j]) >= 2:
      count += 1

print("Part 1:", count)

# Part 2

# A given claim is special if all of its squares are
# only claimed by it
def is_special(claim):
  ID, xpos, ypos, width, height = claim
  for i in range(xpos, xpos+width):
    for j in range(ypos, ypos+height):
      if len(fabric[i][j]) > 1:
        return False
  return True

# Search for the special claim
for claim in claims:
  if is_special(claim):
    break

print("Part 2:", claim[0])
