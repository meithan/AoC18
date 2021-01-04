# Day 25: Four-Dimensional Adventure

import sys

# ------------------------------------------------------------------------------

def manhattan_dist(p1, p2):
  return sum([abs(p1[i]-p2[i]) for i in range(4)])

# ------------------------------

if len(sys.argv) == 1:
  sys.argv.append(sys.argv[0].replace(".py", ".in"))

points = set()
with open(sys.argv[1]) as f:
  for line in f:
    points.add(tuple(int(x) for x in line.strip().split(",")))

# --------------------------------------
# Part 1

constellations = []
while len(points) > 0:

  q = []
  q.append(points.pop())

  const = []
  while len(q) > 0:

    p = q.pop()
    const.append(p)

    for p1 in list(points):
      if manhattan_dist(p, p1) <= 3:
        q.append(p1)
        points.remove(p1)

  constellations.append(const)

print("Part 1:", len(constellations))

# --------------------------------------
# No Part 2
