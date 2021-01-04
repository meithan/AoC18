# Day 25: Four-Dimensional Adventure

import sys

# ------------------------------------------------------------------------------

def manhattan_dist(p1, p2):
  return sum([abs(p1[i]-p2[i]) for i in range(4)])

def belongs_to(p1, constellation):
  for p2 in constellation:
    if manhattan_dist(p1, p2) <= 3:
      return True
  return False

def can_merge(const1, const2):
  for p1 in const1:
    if belongs_to(p1, const2):
      return True
  return False

def find_merge(constellations):
  new_consts = []
  for i in range(len(constellations)):
    for j in range(i+1,len(constellations)):
      if i != j:
        if can_merge(constellations[i], constellations[j]):
          return (i,j)
  return None

# ------------------------------

if len(sys.argv) == 1:
  sys.argv.append(sys.argv[0].replace(".py", ".in"))

points = []
with open(sys.argv[1]) as f:
  for line in f:
    points.append(tuple(int(x) for x in line.strip().split(",")))

# --------------------------------------
# Part 1

constellations = [[p] for p in points]

while True:
  pair = find_merge(constellations)
  if pair is None:
    break
  i,j = pair
  new_consts = [constellations[i]+constellations[j]]
  for k in range(len(constellations)):
    if k not in pair:
      new_consts.append(constellations[k])
  constellations = new_consts

print("Part 1:", len(constellations))

# --------------------------------------
# No Part 2
