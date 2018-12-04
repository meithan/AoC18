import re

claims = []
with open("day3.in") as f:
  pattern = r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
  for line in f:
    match = re.match(pattern, line.strip())
    claims.append([int(x) for x in match.groups(1)])

N = 1000
fabric = [[] for i in range(N)]
for i in range(N):
  for j in range(N):
    fabric[i].append([])

for ID, xpos, ypos, width, height in claims:
  for i in range(xpos, xpos+width):
    for j in range(ypos, ypos+height):
      fabric[i][j].append(ID)

count = 0
for i in range(N):
  for j in range(N):
    if len(fabric[i][j]) >= 2:
      count += 1
print("Part 1:", count)

def is_special(ID, xpos, ypos, width, height):
  for i in range(xpos, xpos+width):
    for j in range(ypos, ypos+height):
      for k in range(len(fabric[i][j])):
        if fabric[i][j][k] != ID:
          return False
  return True

for claim in claims:
  if is_special(*claim):
    break
print("Part 2:", claim[0])
